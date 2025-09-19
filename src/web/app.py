"""
Main Flask application
"""
from flask import Flask
import os

from ..core.data_handler import DataHandler
from .routes import WebRoutes


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
    
    # Initialize data handler
    data_handler = DataHandler()
    
    # Register routes
    WebRoutes(app, data_handler)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
