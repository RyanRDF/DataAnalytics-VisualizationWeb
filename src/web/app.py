"""
Main Flask application
"""
from flask import Flask
import os
import logging

from core.data_handler import DataHandler
from core.database import init_db, db
from .routes import WebRoutes
from .filters import jakarta_time, jakarta_time_short, jakarta_date

logger = logging.getLogger(__name__)


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    UPLOAD_FOLDER = 'instance/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Initialize database
    init_db(app)
    
    # Create tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully!")
        except Exception as e:
            logger.error(f"Database connection error: {e}", exc_info=True)
    
    # Register custom filters
    app.jinja_env.filters['jakarta_time'] = jakarta_time
    app.jinja_env.filters['jakarta_time_short'] = jakarta_time_short
    app.jinja_env.filters['jakarta_date'] = jakarta_date
    
    # Initialize data handler
    data_handler = DataHandler()
    
    # Register routes
    WebRoutes(app, data_handler)
    
    return app


if __name__ == '__main__':
    app = create_app()
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
