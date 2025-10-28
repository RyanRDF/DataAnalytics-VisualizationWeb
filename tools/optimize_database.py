#!/usr/bin/env python3
"""
Database Performance Optimization Script
Menjalankan optimasi database untuk meningkatkan performa dengan data besar
"""
import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_sql_file(sql_file_path):
    """Run SQL file using psql"""
    try:
        # Database connection parameters
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_NAME = 'DAV'
        DB_USER = 'postgres'
        DB_PASSWORD = 'admin'
        
        # Run SQL file
        cmd = [
            'psql',
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
            '-f', str(sql_file_path)
        ]
        
        print(f"Running SQL file: {sql_file_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SQL file executed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("❌ Error executing SQL file:")
            print("Error:", result.stderr)
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error running SQL file: {e}")
        return False

def check_database_connection():
    """Check if database connection is available"""
    try:
        from src.core.database import db
        from src.web.app import create_app
        
        app = create_app()
        with app.app_context():
            # Test connection
            db.session.execute('SELECT 1')
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main optimization function"""
    print("🚀 Starting Database Performance Optimization")
    print("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        print("❌ Cannot connect to database. Please check your database configuration.")
        return
    
    # Get SQL file path
    sql_file = project_root / "migrations" / "add_performance_indexes.sql"
    
    if not sql_file.exists():
        print(f"❌ SQL file not found: {sql_file}")
        return
    
    # Run optimization
    print(f"📊 Running database optimization...")
    if run_sql_file(sql_file):
        print("✅ Database optimization completed successfully!")
        print("\n📈 Performance improvements:")
        print("- Added indexes for common filter columns")
        print("- Added composite indexes for filter combinations")
        print("- Added indexes for sorting performance")
        print("- Updated table statistics")
        print("\n🎯 Expected improvements:")
        print("- 3-5x faster query performance")
        print("- Better handling of large datasets (10,000+ records)")
        print("- Improved user experience")
    else:
        print("❌ Database optimization failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()




