#!/usr/bin/env python3
"""
Tool untuk menghapus user dengan aman
"""

import sys
from datetime import datetime
from src.core.database import db, User, UserSession, DataUploadLog
from src.web.app import create_app

def delete_user_safely(user_id=None, email=None):
    """Hapus user dengan aman (hapus semua data terkait)"""
    print("🗑️  DELETE USER TOOL")
    print("=" * 40)
    
    # Cari user
    if user_id:
        user = User.query.get(user_id)
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        print("❌ Harus provide user_id atau email!")
        return False
    
    if not user:
        print("❌ User tidak ditemukan!")
        return False
    
    print(f"👤 User ditemukan: {user.name}")
    print(f"📧 Email: {user.email}")
    print(f"🆔 ID: {user.id}")
    
    # Tampilkan data terkait
    sessions = UserSession.query.filter_by(user_id=user.id).all()
    uploads = DataUploadLog.query.filter_by(user_id=user.id).all()
    
    print(f"\n📊 Data terkait:")
    print(f"   - Sessions: {len(sessions)}")
    print(f"   - Upload logs: {len(uploads)}")
    
    # Konfirmasi
    print(f"\n⚠️  PERINGATAN: Aksi ini akan menghapus:")
    print(f"   - User: {user.name} ({user.email})")
    print(f"   - {len(sessions)} session(s)")
    print(f"   - {len(uploads)} upload log(s)")
    print(f"   - Semua data terkait")
    
    confirm = input("\nYakin ingin menghapus? (ketik 'DELETE' untuk konfirmasi): ").strip()
    if confirm != 'DELETE':
        print("❌ Penghapusan dibatalkan.")
        return False
    
    try:
        # Hapus data terkait terlebih dahulu
        print("\n🔄 Menghapus data terkait...")
        
        # Hapus sessions
        if sessions:
            for session in sessions:
                db.session.delete(session)
            print(f"   ✅ {len(sessions)} session(s) dihapus")
        
        # Hapus upload logs
        if uploads:
            for upload in uploads:
                db.session.delete(upload)
            print(f"   ✅ {len(uploads)} upload log(s) dihapus")
        
        # Hapus user
        db.session.delete(user)
        print(f"   ✅ User {user.name} dihapus")
        
        # Commit perubahan
        db.session.commit()
        
        print("\n✅ User berhasil dihapus!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saat menghapus user: {e}")
        db.session.rollback()
        return False

def list_users():
    """List semua user dengan info detail"""
    print("👥 DAFTAR USER")
    print("=" * 40)
    
    users = User.query.all()
    if not users:
        print("❌ Tidak ada user ditemukan!")
        return
    
    print(f"📊 Total user: {len(users)}")
    print("-" * 40)
    
    for i, user in enumerate(users, 1):
        sessions = UserSession.query.filter_by(user_id=user.id).count()
        uploads = DataUploadLog.query.filter_by(user_id=user.id).count()
        
        status = "✅ Aktif" if user.is_active else "❌ Tidak Aktif"
        print(f"{i}. {user.name}")
        print(f"   📧 Email: {user.email}")
        print(f"   🆔 ID: {user.id}")
        print(f"   📊 Status: {status}")
        print(f"   🔐 Sessions: {sessions}")
        print(f"   📁 Uploads: {uploads}")
        print(f"   📅 Dibuat: {user.created_at}")
        print(f"   🕐 Login Terakhir: {user.last_login}")
        print()

def delete_user_by_id():
    """Hapus user berdasarkan ID"""
    print("🗑️  DELETE USER BY ID")
    print("=" * 40)
    
    try:
        user_id = int(input("Masukkan User ID: "))
        return delete_user_safely(user_id=user_id)
    except ValueError:
        print("❌ ID harus berupa angka!")
        return False

def delete_user_by_email():
    """Hapus user berdasarkan email"""
    print("🗑️  DELETE USER BY EMAIL")
    print("=" * 40)
    
    email = input("Masukkan Email: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return False
    
    return delete_user_safely(email=email)

def cleanup_expired_sessions():
    """Bersihkan session yang sudah expired"""
    print("🧹 CLEANUP EXPIRED SESSIONS")
    print("=" * 40)
    
    try:
        # Hapus session yang sudah expired
        expired_sessions = UserSession.query.filter(
            UserSession.expires_at < datetime.utcnow()
        ).all()
        
        if not expired_sessions:
            print("✅ Tidak ada session expired yang perlu dibersihkan.")
            return True
        
        print(f"📊 Ditemukan {len(expired_sessions)} session expired")
        
        for session in expired_sessions:
            db.session.delete(session)
        
        db.session.commit()
        print(f"✅ {len(expired_sessions)} session expired dihapus")
        return True
        
    except Exception as e:
        print(f"❌ Error saat cleanup: {e}")
        db.session.rollback()
        return False

def main():
    """Main function"""
    print("🏥 DAV USER MANAGEMENT TOOL")
    print("=" * 50)
    
    while True:
        print("\nMenu:")
        print("1. List semua user")
        print("2. Hapus user by ID")
        print("3. Hapus user by Email")
        print("4. Cleanup expired sessions")
        print("5. Keluar")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            list_users()
        elif choice == '2':
            delete_user_by_id()
        elif choice == '3':
            delete_user_by_email()
        elif choice == '4':
            cleanup_expired_sessions()
        elif choice == '5':
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
