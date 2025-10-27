"""
Flask routes for the web application
"""
from flask import render_template, request, redirect, url_for, jsonify, session
from typing import Dict, Any
from datetime import datetime, timedelta
from utils.timezone_utils import jakarta_now
from functools import wraps

from core.data_handler import DataHandler
from core.database import db, User, UserSession, LoginLog, UploadLog, UserActivityLog, RegistrationCode
from core.robust_data_extractor import RobustDataExtractor
from core.upload_service import UploadService


class WebRoutes:
    """Web routes handler using OOP pattern"""
    
    def __init__(self, app, data_handler: DataHandler):
        self.app = app
        self.data_handler = data_handler
        self.robust_extractor = RobustDataExtractor()
        self.upload_service = UploadService()
        self._register_routes()
    
    def login_required(self, f):
        """Decorator to require login for routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            session_token = session.get('session_token')
            
            if not user_id or not session_token:
                return redirect(url_for('login'))
            
            # Verify session is still valid
            user_session = UserSession.query.filter_by(
                user_id=user_id,
                session_token=session_token,
                is_active=True
            ).filter(UserSession.expires_at > jakarta_now()).first()
            
            if not user_session:
                session.clear()
                return redirect(url_for('login'))
            
            return f(*args, **kwargs)
        return decorated_function
        
    def api_login_required(self, f):
        """Decorator to require login for API routes (returns JSON)"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            session_token = session.get('session_token')
            
            if not user_id or not session_token:
                return jsonify({
                    'success': False,
                    'message': 'Anda harus login terlebih dahulu!'
                }), 401
            
            # Verify session is still valid
            user_session = UserSession.query.filter_by(
                user_id=user_id,
                session_token=session_token,
                is_active=True
            ).filter(UserSession.expires_at > jakarta_now()).first()
            
            if not user_session:
                session.clear()
                return jsonify({
                    'success': False,
                    'message': 'Session expired. Silakan login kembali!'
                }), 401
            
            return f(*args, **kwargs)
        return decorated_function
    
    def _register_routes(self):
        """Register all Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('login.html')
        
        @self.app.route('/login')
        def login():
            return render_template('login.html')
        
        @self.app.route('/main')
        @self.login_required
        def main():
            # Get current user and session info
            user_id = session.get('user_id')
            session_token = session.get('session_token')
            
            user = User.query.get(user_id)
            user_session = UserSession.query.filter_by(
                user_id=user_id,
                session_token=session_token,
                is_active=True
            ).first()
            
            return render_template('index.html', 
                                 table_html="", 
                                 has_data=False,
                                 current_user=user,
                                 user_session=user_session)
        
        @self.app.route('/auth/login', methods=['POST'])
        def auth_login():
            """Handle login authentication with database"""
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            remember_me = data.get('remember_me', False)
            
            # Get client info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            
            if not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Email dan password harus diisi!'
                }), 400
            
            # Find user in database
            user = User.query.filter_by(email=email, is_active=True).first()
            
            if user and user.check_password(password):
                # Update last login
                user.last_login = jakarta_now()
                
                # Create session
                session_token = user.create_session(ip_address=ip_address, user_agent=user_agent)
                
                # Log successful login
                login_log = LoginLog(
                    user_id=user.user_id,
                    username=user.username,
                    email=user.email,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status='success'
                )
                db.session.add(login_log)
                
                # Log activity
                user.log_activity(
                    activity_type='login',
                    description='User logged in successfully',
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                db.session.commit()
                
                response_data = {
                    'success': True,
                    'message': 'Login berhasil!',
                    'user': user.to_dict(),
                    'session_token': session_token
                }
                
                # Set session
                session['user_id'] = user.user_id
                session['session_token'] = session_token
                
                return jsonify(response_data)
            else:
                # Log failed login attempt
                login_log = LoginLog(
                    username=email,  # Store attempted email as username
                    email=email,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status='failed',
                    failure_reason='Invalid credentials'
                )
                db.session.add(login_log)
                db.session.commit()
                
                return jsonify({
                    'success': False,
                    'message': 'Email atau password tidak valid!'
                }), 400
        
        @self.app.route('/auth/register', methods=['POST'])
        def auth_register():
            """Handle user registration"""
            data = request.get_json()
            username = data.get('username')
            full_name = data.get('full_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            registration_code = data.get('registration_code')
            
            # Get client info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            
            # Validate input
            if not username or len(username) < 3:
                return jsonify({
                    'success': False,
                    'message': 'Username minimal 3 karakter'
                }), 400
            
            if not full_name or len(full_name) < 2:
                return jsonify({
                    'success': False,
                    'message': 'Nama lengkap minimal 2 karakter'
                }), 400
            
            if not email or '@' not in email:
                return jsonify({
                    'success': False,
                    'message': 'Format email tidak valid'
                }), 400
            
            if not password or len(password) < 6:
                return jsonify({
                    'success': False,
                    'message': 'Password minimal 6 karakter'
                }), 400
            
            if password != confirm_password:
                return jsonify({
                    'success': False,
                    'message': 'Password tidak sama'
                }), 400
            
            # Validate registration code
            if not registration_code:
                return jsonify({
                    'success': False,
                    'message': 'Kode registrasi harus diisi!'
                }), 400
            
            # Check registration code
            reg_code = RegistrationCode.query.filter_by(
                code=registration_code,
                is_used=False,
                is_active=True
            ).filter(RegistrationCode.expires_at > jakarta_now()).first()
            
            if not reg_code:
                return jsonify({
                    'success': False,
                    'message': 'Kode registrasi tidak valid atau sudah kadaluarsa!'
                }), 400
            
            # Check if user already exists
            existing_user = User.query.filter(
                (User.email == email) | (User.username == username)
            ).first()
            if existing_user:
                if existing_user.email == email:
                    return jsonify({
                        'success': False,
                        'message': 'Email sudah terdaftar!'
                    }), 400
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Username sudah digunakan!'
                    }), 400
            
            # Create new user
            try:
                user = User(
                    username=username,
                    full_name=full_name,
                    email=email,
                    role=reg_code.role  # Use role from registration code
                )
                user.set_password(password)
                
                db.session.add(user)
                db.session.flush()  # Get user ID
                
                # Mark registration code as used
                reg_code.is_used = True
                reg_code.used_by = user.user_id
                reg_code.used_at = jakarta_now()
                
                db.session.commit()
                
                # Log registration activity
                user.log_activity(
                    activity_type='register',
                    description=f'User registered successfully with role {reg_code.role}',
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                return jsonify({
                    'success': True,
                    'message': 'Registrasi berhasil! Silakan login dengan akun baru Anda.',
                    'user': user.to_dict()
                })
            
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': 'Terjadi kesalahan saat registrasi!'
                }), 500
        
        @self.app.route('/auth/logout', methods=['POST'])
        def auth_logout():
            """Handle user logout"""
            # Get client info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            
            # Get current user
            user_id = session.get('user_id')
            session_token = session.get('session_token')
            
            if user_id and session_token:
                # Find user session
                user_session = UserSession.query.filter_by(
                    user_id=user_id,
                    session_token=session_token,
                    is_active=True
                ).first()
                
                if user_session:
                    # Deactivate session
                    user_session.is_active = False
                    user_session.logout_time = jakarta_now()
                    
                    # Log logout activity
                    user = User.query.get(user_id)
                    if user:
                        user.log_activity(
                            activity_type='logout',
                            description='User logged out',
                            ip_address=ip_address,
                            user_agent=user_agent,
                            session_id=user_session.session_id
                        )
                    
                    db.session.commit()
            
            # Clear session
            session.clear()
            
            return jsonify({
                'success': True,
                'message': 'Logout berhasil!'
            })
        
        @self.app.route('/upload', methods=['POST'])
        @self.api_login_required
        def upload_file():
            # Get user info from session (already validated by login_required decorator)
            user_id = session.get('user_id')
            session_token = session.get('session_token')
            
            # Check if user has permission to upload (not viewer)
            current_user = User.query.get(user_id)
            if current_user and current_user.role == 'viewer':
                return render_template('index.html', table_html="", has_data=False, 
                                     error="Akses ditolak. Role viewer tidak dapat mengupload data.")
            
            # Get current user session for logging
            user_session = UserSession.query.filter_by(
                user_id=user_id,
                session_token=session_token,
                is_active=True
            ).first()

            if 'file' not in request.files:
                return redirect(url_for('index'))

            file = request.files['file']
            if file.filename == '':
                return redirect(url_for('index'))

            # Get client info
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            # Validate file
            is_valid, error = self.data_handler.validate_file(file.filename)
            if not is_valid:
                return render_template('index.html', table_html="", has_data=False, error=error)

            try:
                # Save the uploaded file
                filepath, error = self.data_handler.save_uploaded_file(file, self.app.config['UPLOAD_FOLDER'])
                if error:
                    return render_template('index.html', table_html="", has_data=False, error=error)

                # Process file dengan upload service yang baru
                upload_result = self.upload_service.process_upload(filepath, user_id)

                # Upload service sudah menangani logging, jadi kita tidak perlu update upload_log lagi

                # Log upload activity
                user = User.query.get(user_id)
                if user:
                    user.log_activity(
                        activity_type='upload',
                        description=f'Uploaded file: {file.filename}',
                        table_affected='data_analytics',
                        ip_address=ip_address,
                        user_agent=user_agent
                    )

                # Clean up the uploaded file
                self.data_handler.cleanup_file(filepath)

                if not upload_result['success']:
                    return render_template('index.html', table_html="", has_data=False, error=upload_result.get('error', 'Upload gagal'))

                # Get database stats
                from core.database_query_service import DatabaseQueryService
                db_query_service = DatabaseQueryService()
                db_stats = db_query_service.get_database_stats()

                # Show success message with upload stats
                success_message = upload_result.get('message', 'Data berhasil diproses!')

                # Prepare clean upload result for template (remove non-serializable objects)
                clean_upload_result = {
                    'success': upload_result.get('success', False),
                    'rows_success': upload_result.get('rows_success', 0),
                    'rows_failed': upload_result.get('rows_failed', 0),
                    'total_rows': upload_result.get('total_rows', 0),
                    'message': upload_result.get('message', '')
                }
                
                return render_template('index.html',
                                     table_html="",
                                     has_data=True,
                                     success_message=success_message,
                                     upload_result=clean_upload_result,
                                     db_stats=db_stats)

            except Exception as e:
                return render_template('index.html', table_html="", has_data=False, error=f"Error processing file: {str(e)}")
        
        @self.app.route('/api/data/<view_type>')
        def get_data_api(view_type):
            """API endpoint untuk mengambil data dalam bentuk JSON"""
            try:
                if not self.data_handler.has_data():
                    return jsonify({"error": "No data available"}), 400
                
                handler = self._get_handler(view_type)
                if not handler:
                    return jsonify({"error": f"Handler {view_type} not found"}), 400
                
                # Get table HTML
                table_html, error = handler.get_table()
                if error:
                    return jsonify({"error": error}), 400
                
                return jsonify({
                    "success": True,
                    "table_html": table_html,
                    "view_type": view_type
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/processing-info')
        def processing_info():
            """Get database statistics"""
            from core.database_query_service import DatabaseQueryService
            
            try:
                db_query_service = DatabaseQueryService()
                stats = db_query_service.get_database_stats()
                
                # Get upload logs count
                upload_count = UploadLog.query.filter_by(status='success').count()
                
                # Get LAST upload data (not cumulative)
                last_upload = UploadLog.query.filter_by(status='success').order_by(UploadLog.upload_time.desc()).first()
                
                if last_upload:
                    last_rows_success = last_upload.rows_success or 0
                    last_rows_failed = last_upload.rows_failed or 0
                else:
                    last_rows_success = 0
                    last_rows_failed = 0
                
                return jsonify({
                    'success': True,
                    'has_data': stats.get('total_rows', 0) > 0,
                    'total_rows': stats.get('total_rows', 0),
                    'upload_count': upload_count,
                    'rows_success': int(last_rows_success),  # Last upload only
                    'rows_failed': int(last_rows_failed),    # Last upload only
                    'stats': stats
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/clear-all-data', methods=['POST'])
        def clear_all_data():
            """Clear all database data"""
            try:
                # Import the clear tool
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'tools'))
                from clear_all_tables import clear_all_tables
                
                # Clear all tables
                result = clear_all_tables()
                if result:
                    return jsonify({"message": "All database data cleared successfully"})
                else:
                    return jsonify({"error": "Failed to clear database data"}), 500
            except Exception as e:
                return jsonify({"error": f"Error clearing data: {str(e)}"}), 500
        
        @self.app.route('/accumulation-info')
        def accumulation_info():
            """Get database information"""
            from core.database_query_service import DatabaseQueryService
            db_query_service = DatabaseQueryService()
            db_stats = db_query_service.get_database_stats()
            return jsonify(db_stats)
        
        # Register analysis routes
        self._register_analysis_routes()
        
        # Register admin routes
        self._register_admin_routes()
    
    def _register_analysis_routes(self):
        """Register analysis-specific routes"""
        
        # Financial routes
        @self.app.route('/keuangan')
        def keuangan():
            return self._handle_analysis_route('financial', 'keuangan')
        
        @self.app.route('/keuangan/sort')
        def keuangan_sort():
            return self._handle_sort_route('financial')
        
        @self.app.route('/keuangan/filter')
        def keuangan_filter():
            return self._handle_filter_route('financial')
        
        @self.app.route('/keuangan/columns')
        def keuangan_columns():
            return self._handle_columns_route('financial')
        
        @self.app.route('/keuangan/specific-filter')
        def keuangan_specific_filter():
            return self._handle_specific_filter_route('financial')
        
        # Patient routes
        @self.app.route('/pasien')
        def pasien():
            return self._handle_analysis_route('patient', 'pasien')
        
        @self.app.route('/pasien/sort')
        def pasien_sort():
            return self._handle_sort_route('patient')
        
        @self.app.route('/pasien/filter')
        def pasien_filter():
            return self._handle_filter_route('patient')
        
        @self.app.route('/pasien/columns')
        def pasien_columns():
            return self._handle_columns_route('patient')
        
        @self.app.route('/pasien/specific-filter')
        def pasien_specific_filter():
            return self._handle_specific_filter_route('patient')
        
        # Selisih Tarif routes
        @self.app.route('/selisih-tarif')
        def selisih_tarif():
            return self._handle_analysis_route('selisih_tarif', 'selisih-tarif')
        
        @self.app.route('/selisih-tarif/sort')
        def selisih_tarif_sort():
            return self._handle_sort_route('selisih_tarif')
        
        @self.app.route('/selisih-tarif/filter')
        def selisih_tarif_filter():
            return self._handle_filter_route('selisih_tarif')
        
        @self.app.route('/selisih-tarif/columns')
        def selisih_tarif_columns():
            return self._handle_columns_route('selisih_tarif')
        
        @self.app.route('/selisih-tarif/specific-filter')
        def selisih_tarif_specific_filter():
            return self._handle_specific_filter_route('selisih_tarif')
        
        # LOS routes
        @self.app.route('/los')
        def los():
            return self._handle_analysis_route('los', 'los')
        
        @self.app.route('/los/sort')
        def los_sort():
            return self._handle_sort_route('los')
        
        @self.app.route('/los/filter')
        def los_filter():
            return self._handle_filter_route('los')
        
        @self.app.route('/los/columns')
        def los_columns():
            return self._handle_columns_route('los')
        
        @self.app.route('/los/specific-filter')
        def los_specific_filter():
            return self._handle_specific_filter_route('los')
        
        # INACBG routes
        @self.app.route('/inacbg')
        def inacbg():
            return self._handle_analysis_route('inacbg', 'inacbg')
        
        @self.app.route('/inacbg/sort')
        def inacbg_sort():
            return self._handle_sort_route('inacbg')
        
        @self.app.route('/inacbg/filter')
        def inacbg_filter():
            return self._handle_filter_route('inacbg')
        
        @self.app.route('/inacbg/columns')
        def inacbg_columns():
            return self._handle_columns_route('inacbg')
        
        @self.app.route('/inacbg/specific-filter')
        def inacbg_specific_filter():
            return self._handle_specific_filter_route('inacbg')
        
        # Ventilator routes
        @self.app.route('/ventilator')
        def ventilator():
            return self._handle_analysis_route('ventilator', 'ventilator')
        
        @self.app.route('/ventilator/sort')
        def ventilator_sort():
            return self._handle_sort_route('ventilator')
        
        @self.app.route('/ventilator/filter')
        def ventilator_filter():
            return self._handle_filter_route('ventilator')
        
        @self.app.route('/ventilator/columns')
        def ventilator_columns():
            return self._handle_columns_route('ventilator')
        
        @self.app.route('/ventilator/specific-filter')
        def ventilator_specific_filter():
            return self._handle_specific_filter_route('ventilator')
    
    def _get_handler(self, handler_name: str):
        """Get handler by name"""
        handler_map = {
            'keuangan': self.data_handler.financial_handler,
            'financial': self.data_handler.financial_handler,
            'pasien': self.data_handler.patient_handler,
            'patient': self.data_handler.patient_handler,
            'selisih-tarif': self.data_handler.selisih_tarif_handler,
            'selisih_tarif': self.data_handler.selisih_tarif_handler,
            'los': self.data_handler.los_handler,
            'inacbg': self.data_handler.inacbg_handler,
            'ventilator': self.data_handler.ventilator_handler
        }
        return handler_map.get(handler_name)
    
    def _handle_analysis_route(self, handler_name: str, view_name: str):
        """Handle analysis route"""
        if not self.data_handler.has_data():
            return render_template('index.html', table_html="", has_data=False, 
                                 error="No data available. Please upload a file first.")
        
        handler = self._get_handler(handler_name)
        if not handler:
            return render_template('index.html', table_html="", has_data=False, 
                                 error=f"Handler {handler_name} not found.")
        
        # Get table
        table_html, error = handler.get_table()
        
        if error:
            return render_template('index.html', table_html="", has_data=False, error=error)
        
        return render_template('index.html', table_html=table_html, has_data=True, current_view=view_name)
    
    def _handle_sort_route(self, handler_name: str):
        """Handle sort route"""
        if not self.data_handler.has_data():
            return jsonify({"error": "No data available"}), 400
        
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        sort_column = request.args.get('column')
        sort_order = request.args.get('order', 'ASC')
        
        if not sort_column:
            return jsonify({"error": "Column parameter is required"}), 400
        
        table_html, error = handler.get_table(sort_column, sort_order)
        
        if error:
            return jsonify({"error": error}), 400
        
        return jsonify({"table_html": table_html})
    
    def _handle_filter_route(self, handler_name: str):
        """Handle filter route with flexible filtering - supports any combination of filters"""
        if not self.data_handler.has_data():
            return jsonify({"error": "No data available"}), 400
        
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        # Get all filter parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        sort_column = request.args.get('sort_column')
        sort_order = request.args.get('sort_order', 'ASC')
        filter_column = request.args.get('filter_column')
        filter_value = request.args.get('filter_value')
        
        # Use unified get_table method that supports all filter combinations
        table_html, error = handler.get_table(
            sort_column=sort_column,
            sort_order=sort_order,
            start_date=start_date,
            end_date=end_date,
            filter_column=filter_column,
            filter_value=filter_value
        )
        
        if error:
            return jsonify({"error": error}), 400
        
        return jsonify({"table_html": table_html})
    
    def _handle_columns_route(self, handler_name: str):
        """Handle columns route"""
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        columns = handler.get_columns()
        return jsonify({"columns": columns})
    
    def _handle_specific_filter_route(self, handler_name: str):
        """Handle specific filter route with flexible filtering"""
        if not self.data_handler.has_data():
            return jsonify({"error": "No data available"}), 400
        
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        # Get all filter parameters
        filter_column = request.args.get('filter_column')
        filter_value = request.args.get('filter_value')
        sort_column = request.args.get('sort_column')
        sort_order = request.args.get('sort_order', 'ASC')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Check if specific filter is provided
        if filter_column and filter_value:
            table_html, error = handler.get_table_with_specific_filter(
                filter_column, filter_value, sort_column, sort_order, start_date, end_date
            )
        else:
            # Fallback to regular filter if no specific filter provided
            table_html, error = handler.get_table(sort_column, sort_order, start_date, end_date)
        
        if error:
            return jsonify({"error": error}), 400
        
        return jsonify({"table_html": table_html})
    
    def _register_admin_routes(self):
        """Register admin-specific routes"""
        
        @self.app.route('/admin/users', methods=['GET'])
        @self.api_login_required
        def admin_get_users():
            """Get all users for admin management"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                users = User.query.all()
                users_data = []
                
                for user in users:
                    user_data = user.to_dict()
                    # Add additional info
                    user_data['created_by_name'] = user.creator.username if user.creator else 'System'
                    users_data.append(user_data)
                
                return jsonify({
                    'success': True,
                    'users': users_data
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
        @self.api_login_required
        def admin_reset_user_password(user_id):
            """Reset user password"""
            # Check if current user is admin
            current_user_id = session.get('user_id')
            current_user = User.query.get(current_user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                target_user = User.query.get(user_id)
                if not target_user:
                    return jsonify({
                        'success': False,
                        'message': 'User tidak ditemukan'
                    }), 404
                
                # Generate new password
                import random
                import string
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                # Set new password
                target_user.set_password(new_password)
                target_user.updated_at = jakarta_now()
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Reset password for user {target_user.username}',
                    table_affected='users',
                    record_id=str(user_id),
                    new_values={'password_reset': True}
                )
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Password berhasil direset untuk user {target_user.username}',
                    'new_password': new_password
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
        @self.api_login_required
        def admin_delete_user(user_id):
            """Delete user (soft delete)"""
            # Check if current user is admin
            current_user_id = session.get('user_id')
            current_user = User.query.get(current_user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                target_user = User.query.get(user_id)
                if not target_user:
                    return jsonify({
                        'success': False,
                        'message': 'User tidak ditemukan'
                    }), 404
                
                if target_user.user_id == current_user_id:
                    return jsonify({
                        'success': False,
                        'message': 'Tidak dapat menghapus akun sendiri'
                    }), 400
                
                # Soft delete - deactivate user
                target_user.is_active = False
                target_user.updated_at = jakarta_now()
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Deleted user {target_user.username}',
                    table_affected='users',
                    record_id=str(user_id),
                    old_values={'is_active': True},
                    new_values={'is_active': False}
                )
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'User {target_user.username} berhasil dihapus'
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/registration-codes', methods=['GET'])
        @self.api_login_required
        def admin_get_registration_codes():
            """Get all registration codes"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                codes = RegistrationCode.query.order_by(RegistrationCode.created_at.desc()).all()
                codes_data = []
                
                for code in codes:
                    code_data = code.to_dict()
                    # Add additional info
                    code_data['created_by_name'] = code.creator.username if code.creator else 'System'
                    code_data['used_by_name'] = code.user_who_used.username if code.user_who_used else None
                    codes_data.append(code_data)
                
                return jsonify({
                    'success': True,
                    'codes': codes_data
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/registration-codes/generate', methods=['POST'])
        @self.api_login_required
        def admin_generate_registration_codes():
            """Generate new registration codes"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            data = request.get_json()
            role = data.get('role')
            expiry_days = data.get('expiry_days', 30)
            count = data.get('count', 1)
            
            if not role or role not in ['user', 'viewer', 'admin']:
                return jsonify({
                    'success': False,
                    'message': 'Role tidak valid'
                }), 400
            
            try:
                import random
                import string
                generated_codes = []
                
                for _ in range(count):
                    # Generate unique code
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    
                    # Check if code already exists
                    while RegistrationCode.query.filter_by(code=code).first():
                        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    
                    # Create registration code
                    expires_at = jakarta_now() + timedelta(days=expiry_days)
                    reg_code = RegistrationCode(
                        code=code,
                        role=role,
                        created_by=user_id,
                        expires_at=expires_at
                    )
                    
                    db.session.add(reg_code)
                    generated_codes.append({
                        'code': code,
                        'role': role,
                        'expires_at': expires_at.isoformat()
                    })
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Generated {count} registration codes for role {role}',
                    table_affected='registration_codes',
                    new_values={'codes_generated': count, 'role': role}
                )
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Berhasil generate {count} kode untuk role {role}',
                    'codes': generated_codes
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/registration-codes/<int:code_id>/delete', methods=['POST'])
        @self.api_login_required
        def admin_delete_registration_code(code_id):
            """Delete registration code"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                reg_code = RegistrationCode.query.get(code_id)
                if not reg_code:
                    return jsonify({
                        'success': False,
                        'message': 'Kode registrasi tidak ditemukan'
                    }), 404
                
                if reg_code.is_used:
                    return jsonify({
                        'success': False,
                        'message': 'Tidak dapat menghapus kode yang sudah digunakan'
                    }), 400
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Deleted registration code {reg_code.code}',
                    table_affected='registration_codes',
                    record_id=str(code_id)
                )
                
                db.session.delete(reg_code)
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Kode {reg_code.code} berhasil dihapus'
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/registration-codes/clear-unused', methods=['POST'])
        @self.api_login_required
        def admin_clear_unused_codes():
            """Clear all unused registration codes"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                # Get all unused codes
                unused_codes = RegistrationCode.query.filter_by(
                    is_used=False,
                    is_active=True
                ).all()
                
                if not unused_codes:
                    return jsonify({
                        'success': True,
                        'message': 'Tidak ada kode yang belum digunakan',
                        'deleted_count': 0
                    })
                
                # Count codes to be deleted
                deleted_count = len(unused_codes)
                code_list = [code.code for code in unused_codes]
                
                # Delete all unused codes
                for code in unused_codes:
                    db.session.delete(code)
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Cleared {deleted_count} unused registration codes: {", ".join(code_list)}',
                    table_affected='registration_codes',
                    new_values={'deleted_codes': code_list, 'count': deleted_count}
                )
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Berhasil menghapus {deleted_count} kode yang belum digunakan',
                    'deleted_count': deleted_count,
                    'deleted_codes': code_list
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
        
        @self.app.route('/admin/registration-codes/clear-expired', methods=['POST'])
        @self.api_login_required
        def admin_clear_expired_codes():
            """Clear all expired registration codes"""
            # Check if current user is admin
            user_id = session.get('user_id')
            current_user = User.query.get(user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            try:
                # Get all expired codes
                expired_codes = RegistrationCode.query.filter(
                    RegistrationCode.expires_at < jakarta_now()
                ).all()
                
                if not expired_codes:
                    return jsonify({
                        'success': True,
                        'message': 'Tidak ada kode yang sudah kadaluarsa',
                        'deleted_count': 0
                    })
                
                # Count codes to be deleted
                deleted_count = len(expired_codes)
                code_list = [code.code for code in expired_codes]
                
                # Delete all expired codes
                for code in expired_codes:
                    db.session.delete(code)
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Cleared {deleted_count} expired registration codes: {", ".join(code_list)}',
                    table_affected='registration_codes',
                    new_values={'deleted_codes': code_list, 'count': deleted_count}
                )
                
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': f'Berhasil menghapus {deleted_count} kode yang sudah kadaluarsa',
                    'deleted_count': deleted_count,
                    'deleted_codes': code_list
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'Error: {str(e)}'
                }), 500
