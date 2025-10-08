#!/usr/bin/env python3
"""
Script untuk menjalankan website dengan integrasi database user
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main function to run the website"""
    try:
        from web.app import create_app
        
        print("Starting DAV Website with User Database Integration...")
        print("=" * 60)
        
        # Create Flask app
        app = create_app()
        
        print("Flask app created successfully!")
        print("Website is running at: http://localhost:5000")
        print("Database: PostgreSQL DAV")
        print("User Management: Enabled")
        print("Authentication: Enabled")
        print("Upload Tracking: Enabled")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"Error starting website: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
