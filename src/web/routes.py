"""
Flask routes for the web application
"""
from flask import render_template, request, redirect, url_for, jsonify, session
from typing import Dict, Any
from datetime import datetime

from ..core.data_handler import DataHandler
from ..core.database import db, User


class WebRoutes:
    """Web routes handler using OOP pattern"""
    
    def __init__(self, app, data_handler: DataHandler):
        self.app = app
        self.data_handler = data_handler
        self._register_routes()
    
    def _register_routes(self):
        """Register all Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('login.html')
        
        @self.app.route('/login')
        def login():
            return render_template('login.html')
        
        @self.app.route('/main')
        def main():
            return render_template('index.html', table_html="", has_data=False)
        
        @self.app.route('/auth/login', methods=['POST'])
        def auth_login():
            """Handle login authentication with database"""
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            remember_me = data.get('remember_me', False)
            
            if not email or not password:
                return jsonify({
                    'success': False,
                    'message': 'Email dan password harus diisi!'
                }), 400
            
            # Find user in database
            user = User.query.filter_by(email=email, is_active=True).first()
            
            if user and user.check_password(password):
                # Update last login
                user.last_login = datetime.utcnow()
                
                # Create session
                session_token = user.create_session()
                
                db.session.commit()
                
                response_data = {
                    'success': True,
                    'message': 'Login berhasil!',
                    'user': user.to_dict(),
                    'session_token': session_token
                }
                
                # Set session
                session['user_id'] = user.id
                session['session_token'] = session_token
                
                return jsonify(response_data)
            else:
                return jsonify({
                    'success': False,
                    'message': 'Email atau password tidak valid!'
                }), 400
        
        @self.app.route('/auth/register', methods=['POST'])
        def auth_register():
            """Handle user registration"""
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            # Validate input
            if not name or len(name) < 2:
                return jsonify({
                    'success': False,
                    'message': 'Nama minimal 2 karakter'
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
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email sudah terdaftar!'
                }), 400
            
            # Create new user
            try:
                user = User(name=name, email=email)
                user.set_password(password)
                
                db.session.add(user)
                db.session.commit()
                
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
            # Clear session or JWT token here
            return jsonify({
                'success': True,
                'message': 'Logout berhasil!'
            })
        
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            if 'file' not in request.files:
                return redirect(url_for('index'))
            
            file = request.files['file']
            if file.filename == '':
                return redirect(url_for('index'))
            
            # Validate file
            is_valid, error = self.data_handler.validate_file(file.filename)
            if not is_valid:
                return render_template('index.html', table_html="", has_data=False, error=error)
            
            try:
                # Save the uploaded file
                filepath, error = self.data_handler.save_uploaded_file(file, self.app.config['UPLOAD_FOLDER'])
                if error:
                    return render_template('index.html', table_html="", has_data=False, error=error)
                
                # Load data from file
                df, error = self.data_handler.load_data_from_file(filepath)
                if error:
                    self.data_handler.cleanup_file(filepath)
                    return render_template('index.html', table_html="", has_data=False, error=error)
                
                # Get processed data table
                table_html, has_data = self.data_handler.get_raw_data_table()
                
                # Get processing summary
                processing_summary = self.data_handler.get_processing_summary()
                
                # Clean up the uploaded file
                self.data_handler.cleanup_file(filepath)
                
                return render_template('index.html', table_html=table_html, has_data=has_data, processing_summary=processing_summary)
                
            except Exception as e:
                return render_template('index.html', table_html="", has_data=False, error=f"Error processing file: {str(e)}")
        
        @self.app.route('/processing-info')
        def processing_info():
            """Get data processing summary"""
            if not self.data_handler.has_data():
                return jsonify({"error": "No data available"}), 400
            
            processing_summary = self.data_handler.get_processing_summary()
            return jsonify(processing_summary)
        
        @self.app.route('/clear-all-data', methods=['POST'])
        def clear_all_data():
            """Clear all accumulated data"""
            self.data_handler.clear_all_data()
            return jsonify({"message": "All data cleared successfully"})
        
        @self.app.route('/accumulation-info')
        def accumulation_info():
            """Get data accumulation information"""
            accumulation_info = self.data_handler.get_accumulation_info()
            return jsonify(accumulation_info)
        
        # Register analysis routes
        self._register_analysis_routes()
    
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
            'financial': self.data_handler.financial_handler,
            'patient': self.data_handler.patient_handler,
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
        """Handle filter route"""
        if not self.data_handler.has_data():
            return jsonify({"error": "No data available"}), 400
        
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        sort_column = request.args.get('sort_column')
        sort_order = request.args.get('sort_order', 'ASC')
        
        table_html, error = handler.get_table(sort_column, sort_order, start_date, end_date)
        
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
        """Handle specific filter route"""
        if not self.data_handler.has_data():
            return jsonify({"error": "No data available"}), 400
        
        handler = self._get_handler(handler_name)
        if not handler:
            return jsonify({"error": f"Handler {handler_name} not found"}), 400
        
        filter_column = request.args.get('filter_column')
        filter_value = request.args.get('filter_value')
        sort_column = request.args.get('sort_column')
        sort_order = request.args.get('sort_order', 'ASC')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not filter_column or not filter_value:
            return jsonify({"error": "Filter column and value are required"}), 400
        
        table_html, error = handler.get_table_with_specific_filter(
            filter_column, filter_value, sort_column, sort_order, start_date, end_date
        )
        
        if error:
            return jsonify({"error": error}), 400
        
        return jsonify({"table_html": table_html})
