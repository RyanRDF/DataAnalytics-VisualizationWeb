#!/usr/bin/env python3
"""
Script untuk menjalankan migrasi database rumah sakit
Database: DAV (Data Analytics Visualization)
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Konfigurasi database
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'DAV',
    'user': 'postgres',
    'password': 'admin'
}

def connect_database():
    """Membuat koneksi ke database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def run_migration():
    """Menjalankan script migrasi"""
    print("🚀 Starting Hospital Database Migration...")
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗄️  Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print("-" * 60)
    
    # Baca file migrasi
    migration_file = 'migrations/create_hospital_tables.sql'
    
    if not os.path.exists(migration_file):
        print(f"❌ Migration file not found: {migration_file}")
        return False
    
    # Koneksi ke database
    conn = connect_database()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Baca dan eksekusi script migrasi
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print("📖 Reading migration script...")
        print("⚡ Executing migration...")
        
        # Eksekusi script
        cursor.execute(migration_sql)
        conn.commit()
        
        print("✅ Migration completed successfully!")
        
        # Verifikasi tabel
        print("\n🔍 Verifying tables...")
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('pasien', 'dokter', 'diagnosa', 'prosedur', 'kunjungan', 'rincian_biaya', 'kunjungan_diagnosa', 'kunjungan_prosedur')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📊 Found {len(tables)} hospital tables:")
        for table_name, table_type in tables:
            print(f"   - {table_name} ({table_type})")
        
        # Cek jumlah data sample
        print("\n📈 Sample data count:")
        cursor.execute("""
            SELECT 
                'Pasien' as tabel, COUNT(*) as jumlah FROM pasien
            UNION ALL
            SELECT 
                'Dokter' as tabel, COUNT(*) as jumlah FROM dokter
            UNION ALL
            SELECT 
                'Diagnosa' as tabel, COUNT(*) as jumlah FROM diagnosa
            UNION ALL
            SELECT 
                'Prosedur' as tabel, COUNT(*) as jumlah FROM prosedur;
        """)
        
        counts = cursor.fetchall()
        for tabel, jumlah in counts:
            print(f"   - {tabel}: {jumlah} records")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    finally:
        if conn:
            conn.close()
            print("🔌 Database connection closed.")

def check_database_exists():
    """Cek apakah database DAV sudah ada"""
    try:
        # Coba koneksi ke database DAV
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        return True
    except psycopg2.Error:
        return False

def create_database():
    """Membuat database DAV jika belum ada"""
    try:
        # Koneksi ke database postgres default
        config = DB_CONFIG.copy()
        config['database'] = 'postgres'
        
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Cek apakah database sudah ada
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        if cursor.fetchone():
            print(f"✅ Database {DB_CONFIG['database']} already exists.")
        else:
            # Buat database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DB_CONFIG['database'])
            ))
            print(f"✅ Database {DB_CONFIG['database']} created successfully.")
        
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🏥 HOSPITAL DATABASE MIGRATION TOOL")
    print("=" * 60)
    
    # Cek apakah database ada
    if not check_database_exists():
        print(f"⚠️  Database {DB_CONFIG['database']} not found.")
        response = input("Do you want to create it? (y/n): ").lower().strip()
        
        if response == 'y':
            if not create_database():
                print("❌ Failed to create database. Exiting.")
                sys.exit(1)
        else:
            print("❌ Migration cancelled. Database required.")
            sys.exit(1)
    
    # Jalankan migrasi
    if run_migration():
        print("\n🎉 Migration completed successfully!")
        print("📋 Next steps:")
        print("   1. Test the database connection in your Flask app")
        print("   2. Run Flask-Migrate to sync SQLAlchemy models")
        print("   3. Start using the new hospital tables")
    else:
        print("\n💥 Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
