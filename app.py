"""
Main application entry point using the new OOP structure
"""
from src.web.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
