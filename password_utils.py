#!/usr/bin/env python3
"""
Password utilities untuk DAV project
"""

from werkzeug.security import generate_password_hash, check_password_hash
from src.core.database import db, User
import getpass

def create_user_with_password():
    """Membuat user baru dengan password"""
    print("=== CREATE NEW USER ===")
    
    name = input("Nama: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if password != confirm_password:
        print("❌ Password tidak sama!")
        return False
    
    # Buat user baru
    user = User(name=name, email=email)
    user.set_password(password)
    
    print(f"✅ User created: {email}")
    print(f"🔐 Password hash: {user.password_hash}")
    
    return user

def test_password():
    """Test password verification"""
    print("=== TEST PASSWORD ===")
    
    email = input("Email user: ")
    password = getpass.getpass("Password to test: ")
    
    # Cari user
    user = User.query.filter_by(email=email).first()
    if not user:
        print("❌ User tidak ditemukan!")
        return False
    
    # Test password
    if user.check_password(password):
        print("✅ Password benar!")
        return True
    else:
        print("❌ Password salah!")
        return False

def reset_user_password():
    """Reset password user"""
    print("=== RESET PASSWORD ===")
    
    email = input("Email user: ")
    new_password = getpass.getpass("Password baru: ")
    confirm_password = getpass.getpass("Confirm password baru: ")
    
    if new_password != confirm_password:
        print("❌ Password tidak sama!")
        return False
    
    # Cari user
    user = User.query.filter_by(email=email).first()
    if not user:
        print("❌ User tidak ditemukan!")
        return False
    
    # Reset password
    user.set_password(new_password)
    
    try:
        db.session.commit()
        print("✅ Password berhasil direset!")
        print(f"🔐 Password hash baru: {user.password_hash}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()
        return False

def show_user_info():
    """Tampilkan info user dan hash password"""
    print("=== USER INFO ===")
    
    email = input("Email user: ")
    
    # Cari user
    user = User.query.filter_by(email=email).first()
    if not user:
        print("❌ User tidak ditemukan!")
        return False
    
    print(f"👤 Nama: {user.name}")
    print(f"📧 Email: {user.email}")
    print(f"🔐 Password Hash: {user.password_hash}")
    print(f"✅ Status: {'Aktif' if user.is_active else 'Tidak Aktif'}")
    print(f"📅 Dibuat: {user.created_at}")
    print(f"🕐 Login Terakhir: {user.last_login}")
    
    return True

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("🔐 PASSWORD UTILITIES - DAV PROJECT")
        print("="*50)
        print("1. Buat user baru")
        print("2. Test password")
        print("3. Reset password")
        print("4. Lihat info user")
        print("5. Keluar")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == '1':
            create_user_with_password()
        elif choice == '2':
            test_password()
        elif choice == '3':
            reset_user_password()
        elif choice == '4':
            show_user_info()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    # Import Flask app context
    from src.web.app import create_app
    
    app = create_app()
    with app.app_context():
        main()
