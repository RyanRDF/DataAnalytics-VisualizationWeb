#!/usr/bin/env python3
"""
Main application entry point for Data Analytics Visualization Web
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the Flask application
from web.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Data Analytics Dashboard...")
    print("📊 Access the application at: http://localhost:5000")
    print("🔐 Default login: admin@ihc.com / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
