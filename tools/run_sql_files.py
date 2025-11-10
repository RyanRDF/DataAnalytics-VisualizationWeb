#!/usr/bin/env python3
"""
Utility untuk menjalankan beberapa file SQL berurutan ke database PostgreSQL

Penggunaan:
  python tools/run_sql_files.py migrations/normalize_users_and_sessions.sql migrations/normalize_logs.sql migrations/normalize_data_analytics.sql migrations/drop_registration_codes.sql

Jika argumen tidak diberikan, script akan menjalankan keempat file di atas (jika ada).
"""
import os
import sys
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'DAV',
    'user': 'postgres',
    'password': 'admin',
}

def run_sql_file(conn, path):
    with open(path, 'r', encoding='utf-8') as f:
        sql_text = f.read()
    with conn.cursor() as cur:
        cur.execute(sql_text)

def main():
    default_files = [
        os.path.join('migrations', 'normalize_users_and_sessions.sql'),
        os.path.join('migrations', 'normalize_logs.sql'),
        os.path.join('migrations', 'normalize_data_analytics.sql'),
        os.path.join('migrations', 'drop_registration_codes.sql'),
    ]

    files = sys.argv[1:] or default_files
    files = [f for f in files if os.path.exists(f)]
    if not files:
        print('Tidak ada file SQL yang ditemukan untuk dijalankan.')
        sys.exit(1)

    print('Menjalankan file SQL (berurutan):')
    for f in files:
        print(f' - {f}')

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
    except Exception as e:
        print(f'Gagal konek database: {e}')
        sys.exit(1)

    try:
        for path in files:
            print(f'Eksekusi: {path} ...')
            run_sql_file(conn, path)
            print('Sukses')
        print('Semua file SQL berhasil dijalankan.')
    except Exception as e:
        print(f'Gagal menjalankan SQL: {e}')
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    main()






