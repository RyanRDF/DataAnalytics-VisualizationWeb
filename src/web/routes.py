"""
Flask routes for the web application
"""
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, session
from typing import Dict, Any
from datetime import datetime, timedelta
from utils.timezone_utils import jakarta_now
from utils.session_utils import login_required, api_login_required, get_valid_user_session
from utils.handler_registry import HandlerRegistry

from core.data_handler import DataHandler
from core.database import db, User, UserSession, LoginLog, UploadLog, UserActivityLog
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
        @login_required(redirect_on_fail=True)
        def main():
            # Get current user and session info
            user_id, user_session = get_valid_user_session()
            
            user = User.query.get(user_id) if user_id else None
            
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
            
            # Registration code dihapus; registrasi tidak lagi memerlukan kode
            
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
                    role='user'
                )
                user.set_password(password)
                
                db.session.add(user)
                db.session.flush()  # Get user ID
                
                # Tidak ada penandaan kode registrasi (fitur dihapus)
                
                db.session.commit()
                
                # Log registration activity
                user.log_activity(
                    activity_type='register',
                    description='User registered successfully with default role user',
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
        @api_login_required
        def upload_file():
            # Get user info from session (already validated by login_required decorator)
            user_id, user_session = get_valid_user_session()
            
            # Check if user has permission to upload (not viewer)
            current_user = User.query.get(user_id) if user_id else None
            if current_user and current_user.role == 'viewer':
                return render_template('index.html', table_html="", has_data=False, 
                                     error="Akses ditolak. Role viewer tidak dapat mengupload data.")

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
        """Register analysis-specific routes dynamically"""
        # Define all handlers and their route prefixes
        handlers = ['financial', 'patient', 'selisih_tarif', 'los', 'inacbg', 'ventilator']
        
        for handler_name in handlers:
            view_name = HandlerRegistry.get_view_name(handler_name)
            
            # Create unique endpoint names to avoid conflicts
            endpoint_prefix = f"{handler_name}_{view_name}"
            
            # Capture values in closure to avoid late binding issues
            def make_route_handler(h_name, v_name):
                return lambda: self._handle_analysis_route(h_name, v_name)
            
            def make_sort_handler(h_name):
                return lambda: self._handle_sort_route(h_name)
            
            def make_filter_handler(h_name):
                return lambda: self._handle_filter_route(h_name)
            
            def make_columns_handler(h_name):
                return lambda: self._handle_columns_route(h_name)
            
            def make_specific_filter_handler(h_name):
                return lambda: self._handle_specific_filter_route(h_name)
            
            # Main view route
            self.app.add_url_rule(
                f'/{view_name}',
                endpoint=f'{endpoint_prefix}_view',
                view_func=make_route_handler(handler_name, view_name)
            )
            
            # Sort route
            self.app.add_url_rule(
                f'/{view_name}/sort',
                endpoint=f'{endpoint_prefix}_sort',
                view_func=make_sort_handler(handler_name)
            )
            
            # Filter route
            self.app.add_url_rule(
                f'/{view_name}/filter',
                endpoint=f'{endpoint_prefix}_filter',
                view_func=make_filter_handler(handler_name)
            )
            
            # Columns route
            self.app.add_url_rule(
                f'/{view_name}/columns',
                endpoint=f'{endpoint_prefix}_columns',
                view_func=make_columns_handler(handler_name)
            )
            
            # Specific filter route
            self.app.add_url_rule(
                f'/{view_name}/specific-filter',
                endpoint=f'{endpoint_prefix}_specific_filter',
                view_func=make_specific_filter_handler(handler_name)
            )
    
    def _get_handler(self, handler_name: str):
        """Get handler by name using centralized registry"""
        return HandlerRegistry.get_handler(self.data_handler, handler_name)
    
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
        @api_login_required
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

        @self.app.route('/admin/users/create', methods=['POST'])
        @api_login_required
        def admin_create_user():
            """Admin creates a new user account"""
            current_user_id = session.get('user_id')
            current_user = User.query.get(current_user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            data = request.get_json()
            username = data.get('username')
            full_name = data.get('full_name')
            email = data.get('email')
            role = data.get('role', 'user')
            password = data.get('password')
            
            if not username or not full_name or not email:
                return jsonify({'success': False, 'message': 'Username, nama lengkap, dan email wajib diisi'}), 400
            
            # Disallow creating admin via API
            if role not in ['user', 'viewer']:
                return jsonify({'success': False, 'message': 'Role tidak valid. Role admin hanya dibuat manual di database.'}), 400
            
            if not password or len(password) < 6:
                return jsonify({'success': False, 'message': 'Password minimal 6 karakter'}), 400
            
            try:
                # Check uniqueness
                if User.query.filter((User.username==username) | (User.email==email)).first():
                    return jsonify({'success': False, 'message': 'Username atau email sudah digunakan'}), 400
                
                new_user = User(
                    username=username,
                    full_name=full_name,
                    email=email,
                    role=role,
                    created_by=current_user_id
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.flush()
                
                # Log activity
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Created user {username} with role {role}',
                    table_affected='users',
                    record_id=str(new_user.user_id),
                    new_values={'username': username, 'email': email, 'role': role}
                )
                
                db.session.commit()
                return jsonify({'success': True, 'message': 'User berhasil dibuat', 'user': new_user.to_dict()})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

        @self.app.route('/admin/users/<int:user_id>/update', methods=['POST'])
        @api_login_required
        def admin_update_user(user_id):
            """Admin updates user details"""
            current_user_id = session.get('user_id')
            current_user = User.query.get(current_user_id)
            
            if not current_user or current_user.role != 'admin':
                return jsonify({
                    'success': False,
                    'message': 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.'
                }), 403
            
            data = request.get_json()
            full_name = data.get('full_name')
            email = data.get('email')
            role = data.get('role')
            is_active = data.get('is_active')
            password = data.get('password')  # optional
            
            try:
                user = User.query.get(user_id)
                if not user:
                    return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
                
                old_values = user.to_dict()
                
                if full_name:
                    user.full_name = full_name
                if email and email != user.email:
                    # check uniqueness
                    if User.query.filter(User.email==email, User.user_id!=user_id).first():
                        return jsonify({'success': False, 'message': 'Email sudah digunakan'}), 400
                    user.email = email
                # Guardrails for admin role
                if role is not None:
                    if role == 'admin' and user.role != 'admin':
                        return jsonify({'success': False, 'message': 'Tidak boleh mengubah role ke admin melalui aplikasi'}), 403
                    if user.role == 'admin' and role != 'admin':
                        return jsonify({'success': False, 'message': 'Tidak boleh mengubah role admin melalui aplikasi'}), 403
                    if role in ['user', 'viewer'] and user.role != 'admin':
                        user.role = role
                if isinstance(is_active, bool):
                    user.is_active = is_active
                if password:
                    if len(password) < 6:
                        return jsonify({'success': False, 'message': 'Password minimal 6 karakter'}), 400
                    user.set_password(password)
                user.updated_at = jakarta_now()
                
                new_values = user.to_dict()
                
                current_user.log_activity(
                    activity_type='admin_action',
                    description=f'Updated user {user.username}',
                    table_affected='users',
                    record_id=str(user_id),
                    old_values=old_values,
                    new_values=new_values
                )
                
                db.session.commit()
                return jsonify({'success': True, 'message': 'User berhasil diperbarui', 'user': user.to_dict()})
            except Exception as e:
                db.session.rollback()
                return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
        
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
        @api_login_required
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
                if target_user.role == 'admin':
                    return jsonify({
                        'success': False,
                        'message': 'Tidak dapat menghapus user dengan role admin'
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
        
        # Semua endpoint admin terkait registration codes telah dihapus
