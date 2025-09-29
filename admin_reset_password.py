#!/usr/bin/env python3
"""
Admin script untuk reset password user
"""

import sys
import getpass
from src.core.database import db, User
from src.web.app import create_app

def reset_password():
    """Reset password user"""
    print("🔐 ADMIN PASSWORD RESET")
    print("=" * 40)
    
    # Input email
    email = input("Email user yang akan direset: ").strip()
    if not email:
        print("❌ Email tidak boleh kosong!")
        return False
    
    # Cari user
    user = User.query.filter_by(email=email).first()
    if not user:
        print(f"❌ User dengan email '{email}' tidak ditemukan!")
        return False
    
    print(f"👤 User ditemukan: {user.name}")
    print(f"📧 Email: {user.email}")
    print(f"🔐 Hash saat ini: {user.password_hash}")
    
    # Konfirmasi
    confirm = input("\nYakin ingin reset password? (y/n): ").lower().strip()
    if confirm != 'y':
        print("❌ Reset dibatalkan.")
        return False
    
    # Input password baru
    print("\n📝 Masukkan password baru:")
    new_password = getpass.getpass("Password baru: ")
    if not new_password:
        print("❌ Password tidak boleh kosong!")
        return False
    
    confirm_password = getpass.getpass("Konfirmasi password: ")
    if new_password != confirm_password:
        print("❌ Password tidak sama!")
        return False
    
    # Reset password
    try:
        user.set_password(new_password)
        db.session.commit()
        
        print("✅ Password berhasil direset!")
        print(f"🔐 Hash baru: {user.password_hash}")
        return True
        
    except Exception as e:
        print(f"❌ Error saat reset password: {e}")
        db.session.rollback()
        return False

def list_users():
    """List semua user"""
    print("👥 DAFTAR USER")
    print("=" * 40)
    
    users = User.query.all()
    if not users:
        print("❌ Tidak ada user ditemukan!")
        return
    
    print(f"📊 Total user: {len(users)}")
    print("-" * 40)
    
    for i, user in enumerate(users, 1):
        status = "✅ Aktif" if user.is_active else "❌ Tidak Aktif"
        print(f"{i}. {user.name}")
        print(f"   📧 Email: {user.email}")
        print(f"   🔐 Hash: {user.password_hash}")
        print(f"   📊 Status: {status}")
        print(f"   📅 Dibuat: {user.created_at}")
        print()

def main():
    """Main function"""
    print("🏥 DAV ADMIN TOOL")
    print("=" * 50)
    
    while True:
        print("\nMenu:")
        print("1. Reset password user")
        print("2. List semua user")
        print("3. Keluar")
        
        choice = input("\nPilih menu (1-3): ").strip()
        
        if choice == '1':
            reset_password()
        elif choice == '2':
            list_users()
        elif choice == '3':
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
