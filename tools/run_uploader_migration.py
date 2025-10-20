#!/usr/bin/env python3
"""
Script untuk menjalankan migration menambahkan kolom uploader_id
"""
import sys
import os

# Add src to path
sys.path.append('src')

# Import Flask app untuk application context
from web.app import create_app
from core.database import db
from sqlalchemy import text

def run_migration():
    """Jalankan migration untuk menambahkan kolom uploader_id"""
    app = create_app()
    with app.app_context():
        try:
            print("Starting migration: Add uploader_id column...")
            
            # Read migration SQL
            migration_file = 'migrations/add_uploader_id_column.sql'
            if not os.path.exists(migration_file):
                print(f"Migration file not found: {migration_file}")
                return False
            
            with open(migration_file, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            # Split SQL statements
            statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
            
            # Execute each statement
            for i, statement in enumerate(statements, 1):
                if statement:
                    print(f"Executing statement {i}/{len(statements)}...")
                    try:
                        db.session.execute(text(statement))
                        db.session.commit()
                        print(f"Statement {i} executed successfully")
                    except Exception as e:
                        print(f"Error executing statement {i}: {e}")
                        # Check if column already exists
                        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                            print("Column might already exist, continuing...")
                            continue
                        else:
                            db.session.rollback()
                            return False
            
            print("Migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"Migration failed: {e}")
            db.session.rollback()
            return False

def check_column_exists():
    """Cek apakah kolom uploader_id sudah ada"""
    app = create_app()
    with app.app_context():
        try:
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'data_analytics' 
                AND column_name = 'uploader_id'
            """))
            
            exists = result.fetchone() is not None
            if exists:
                print("Column uploader_id already exists")
            else:
                print("Column uploader_id does not exist")
            
            return exists
            
        except Exception as e:
            print(f"Error checking column: {e}")
            return False

if __name__ == "__main__":
    print("=== Uploader ID Migration Tool ===")
    
    # Check if column already exists
    if check_column_exists():
        print("Column already exists, skipping migration.")
        sys.exit(0)
    
    # Run migration
    success = run_migration()
    
    if success:
        print("Migration completed successfully!")
        sys.exit(0)
    else:
        print("Migration failed!")
        sys.exit(1)
