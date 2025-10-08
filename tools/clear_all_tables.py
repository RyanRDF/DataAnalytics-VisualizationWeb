#!/usr/bin/env python3
"""
Tool untuk mengclear semua isi tabel dengan aman
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from datetime import datetime
from core.database import db, User, UserSession, DataUploadLog, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur
from web.app import create_app

def clear_all_tables():
    """Clear semua isi tabel dengan aman (urutan yang benar untuk FK)"""
    print("🧹 CLEAR ALL TABLES")
    print("=" * 50)
    
    # Urutan penghapusan (dari yang memiliki FK ke yang tidak)
    tables_to_clear = [
        # Tabel dengan foreign key (hapus dulu)
        ("KunjunganDiagnosa", KunjunganDiagnosa),
        ("KunjunganProsedur", KunjunganProsedur),
        ("RincianBiaya", RincianBiaya),
        ("Kunjungan", Kunjungan),
        ("UserSession", UserSession),
        ("DataUploadLog", DataUploadLog),
        
        # Tabel master (hapus terakhir)
        ("Pasien", Pasien),
        ("Dokter", Dokter),
        ("Diagnosa", Diagnosa),
        ("Prosedur", Prosedur),
        ("User", User),
    ]
    
    print("⚠️  PERINGATAN: Aksi ini akan menghapus SEMUA data dari tabel:")
    for table_name, _ in tables_to_clear:
        print(f"   - {table_name}")
    
    print(f"\n📊 Total tabel yang akan di-clear: {len(tables_to_clear)}")
    
    # Konfirmasi
    confirm = input("\nYakin ingin menghapus SEMUA data? (ketik 'CLEAR ALL' untuk konfirmasi): ").strip()
    if confirm != 'CLEAR ALL':
        print("❌ Penghapusan dibatalkan.")
        return False
    
    try:
        print("\n🔄 Memulai penghapusan...")
        
        total_deleted = 0
        for table_name, model in tables_to_clear:
            # Hitung jumlah data sebelum dihapus
            count_before = model.query.count()
            
            if count_before > 0:
                # Hapus semua data
                model.query.delete()
                print(f"   ✅ {table_name}: {count_before} records dihapus")
                total_deleted += count_before
            else:
                print(f"   ⚪ {table_name}: 0 records (sudah kosong)")
        
        # Commit perubahan
        db.session.commit()
        
        print(f"\n✅ Semua tabel berhasil di-clear!")
        print(f"📊 Total records yang dihapus: {total_deleted}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saat menghapus data: {e}")
        db.session.rollback()
        return False

def clear_specific_table():
    """Clear tabel tertentu saja"""
    print("🧹 CLEAR SPECIFIC TABLE")
    print("=" * 50)
    
    # Daftar tabel yang bisa di-clear
    available_tables = {
        "1": ("User", User),
        "2": ("UserSession", UserSession),
        "3": ("DataUploadLog", DataUploadLog),
        "4": ("Pasien", Pasien),
        "5": ("Dokter", Dokter),
        "6": ("Diagnosa", Diagnosa),
        "7": ("Prosedur", Prosedur),
        "8": ("Kunjungan", Kunjungan),
        "9": ("RincianBiaya", RincianBiaya),
        "10": ("KunjunganDiagnosa", KunjunganDiagnosa),
        "11": ("KunjunganProsedur", KunjunganProsedur),
    }
    
    print("Pilih tabel yang ingin di-clear:")
    for key, (name, _) in available_tables.items():
        count = available_tables[key][1].query.count()
        print(f"   {key}. {name} ({count} records)")
    
    choice = input("\nPilih nomor tabel (1-11): ").strip()
    
    if choice not in available_tables:
        print("❌ Pilihan tidak valid!")
        return False
    
    table_name, model = available_tables[choice]
    count_before = model.query.count()
    
    if count_before == 0:
        print(f"✅ Tabel {table_name} sudah kosong!")
        return True
    
    print(f"\n⚠️  Akan menghapus {count_before} records dari tabel {table_name}")
    confirm = input("Yakin? (y/n): ").lower().strip()
    
    if confirm != 'y':
        print("❌ Penghapusan dibatalkan.")
        return False
    
    try:
        # Hapus data
        model.query.delete()
        db.session.commit()
        
        print(f"✅ Tabel {table_name} berhasil di-clear!")
        print(f"📊 {count_before} records dihapus")
        return True
        
    except Exception as e:
        print(f"❌ Error saat menghapus data: {e}")
        db.session.rollback()
        return False

def show_table_counts():
    """Tampilkan jumlah data di setiap tabel"""
    print("📊 TABLE COUNTS")
    print("=" * 50)
    
    tables = [
        ("User", User),
        ("UserSession", UserSession),
        ("DataUploadLog", DataUploadLog),
        ("Pasien", Pasien),
        ("Dokter", Dokter),
        ("Diagnosa", Diagnosa),
        ("Prosedur", Prosedur),
        ("Kunjungan", Kunjungan),
        ("RincianBiaya", RincianBiaya),
        ("KunjunganDiagnosa", KunjunganDiagnosa),
        ("KunjunganProsedur", KunjunganProsedur),
    ]
    
    total_records = 0
    for table_name, model in tables:
        count = model.query.count()
        total_records += count
        status = "📊" if count > 0 else "⚪"
        print(f"{status} {table_name}: {count} records")
    
    print("-" * 50)
    print(f"📈 Total records: {total_records}")

def clear_hospital_tables_only():
    """Clear hanya tabel rumah sakit (tidak termasuk user system)"""
    print("🏥 CLEAR HOSPITAL TABLES ONLY")
    print("=" * 50)
    
    # Hanya tabel rumah sakit
    hospital_tables = [
        ("KunjunganDiagnosa", KunjunganDiagnosa),
        ("KunjunganProsedur", KunjunganProsedur),
        ("RincianBiaya", RincianBiaya),
        ("Kunjungan", Kunjungan),
        ("Pasien", Pasien),
        ("Dokter", Dokter),
        ("Diagnosa", Diagnosa),
        ("Prosedur", Prosedur),
    ]
    
    print("⚠️  Akan menghapus data dari tabel rumah sakit:")
    for table_name, _ in hospital_tables:
        count = hospital_tables[hospital_tables.index((table_name, _))][1].query.count()
        print(f"   - {table_name} ({count} records)")
    
    confirm = input("\nYakin? (ketik 'CLEAR HOSPITAL' untuk konfirmasi): ").strip()
    if confirm != 'CLEAR HOSPITAL':
        print("❌ Penghapusan dibatalkan.")
        return False
    
    try:
        print("\n🔄 Memulai penghapusan...")
        
        total_deleted = 0
        for table_name, model in hospital_tables:
            count_before = model.query.count()
            
            if count_before > 0:
                model.query.delete()
                print(f"   ✅ {table_name}: {count_before} records dihapus")
                total_deleted += count_before
            else:
                print(f"   ⚪ {table_name}: 0 records (sudah kosong)")
        
        db.session.commit()
        
        print(f"\n✅ Tabel rumah sakit berhasil di-clear!")
        print(f"📊 Total records yang dihapus: {total_deleted}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saat menghapus data: {e}")
        db.session.rollback()
        return False

def clear_system_tables_only():
    """Clear hanya tabel sistem (user, session, upload log)"""
    print("🔧 CLEAR SYSTEM TABLES ONLY")
    print("=" * 50)
    
    # Hanya tabel sistem
    system_tables = [
        ("UserSession", UserSession),
        ("DataUploadLog", DataUploadLog),
        ("User", User),
    ]
    
    print("⚠️  Akan menghapus data dari tabel sistem:")
    for table_name, _ in system_tables:
        count = system_tables[system_tables.index((table_name, _))][1].query.count()
        print(f"   - {table_name} ({count} records)")
    
    confirm = input("\nYakin? (ketik 'CLEAR SYSTEM' untuk konfirmasi): ").strip()
    if confirm != 'CLEAR SYSTEM':
        print("❌ Penghapusan dibatalkan.")
        return False
    
    try:
        print("\n🔄 Memulai penghapusan...")
        
        total_deleted = 0
        for table_name, model in system_tables:
            count_before = model.query.count()
            
            if count_before > 0:
                model.query.delete()
                print(f"   ✅ {table_name}: {count_before} records dihapus")
                total_deleted += count_before
            else:
                print(f"   ⚪ {table_name}: 0 records (sudah kosong)")
        
        db.session.commit()
        
        print(f"\n✅ Tabel sistem berhasil di-clear!")
        print(f"📊 Total records yang dihapus: {total_deleted}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saat menghapus data: {e}")
        db.session.rollback()
        return False

def main():
    """Main function"""
    print("🧹 DAV TABLE CLEARING TOOL")
    print("=" * 50)
    
    while True:
        print("\nMenu:")
        print("1. Lihat jumlah data di setiap tabel")
        print("2. Clear tabel tertentu")
        print("3. Clear semua tabel rumah sakit")
        print("4. Clear semua tabel sistem")
        print("5. Clear SEMUA tabel (HATI-HATI!)")
        print("6. Keluar")
        
        choice = input("\nPilih menu (1-6): ").strip()
        
        if choice == '1':
            show_table_counts()
        elif choice == '2':
            clear_specific_table()
        elif choice == '3':
            clear_hospital_tables_only()
        elif choice == '4':
            clear_system_tables_only()
        elif choice == '5':
            clear_all_tables()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    # Buat Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan oleh user.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
