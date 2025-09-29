# 🔐 Password Security - DAV Project

## ⚠️ **PENTING: Hash Password TIDAK BISA DIREVERSE**

Hash password adalah **one-way function** yang dirancang untuk tidak bisa di-reverse ke password asli. Ini adalah fitur keamanan, bukan bug.

## 🔍 **Cara Kerja Hash Password**

### 1. **Saat User Mendaftar/Login**
```python
# Password asli: "mypassword123"
password_hash = generate_password_hash("mypassword123")
# Hasil: "pbkdf2:sha256:260000$abc123$def456..."
```

### 2. **Saat Verifikasi Login**
```python
# User input: "mypassword123"
# Hash tersimpan: "pbkdf2:sha256:260000$abc123$def456..."
is_valid = check_password_hash(stored_hash, "mypassword123")
# Hasil: True/False
```

## 🛠️ **Solusi untuk "Lupa Password"**

### **Opsi 1: Reset Password (Recommended)**
```bash
# Jalankan admin tool
python admin_reset_password.py
```

### **Opsi 2: Manual Reset via Database**
```sql
-- 1. Cari user
SELECT id, name, email, password_hash FROM users WHERE email = 'user@example.com';

-- 2. Update password (hash untuk "newpassword123")
UPDATE users 
SET password_hash = 'pbkdf2:sha256:260000$newhash$newhash...' 
WHERE email = 'user@example.com';
```

### **Opsi 3: Buat User Baru**
```bash
# Jalankan password utils
python password_utils.py
```

## 🔧 **Tools yang Tersedia**

### 1. **Admin Reset Tool** (`admin_reset_password.py`)
```bash
python admin_reset_password.py
```
- Reset password user existing
- List semua user
- Interface yang aman

### 2. **Password Utils** (`password_utils.py`)
```bash
python password_utils.py
```
- Buat user baru
- Test password
- Reset password
- Lihat info user

## 🔐 **Cara Generate Hash Baru**

### **Via Python Script**
```python
from werkzeug.security import generate_password_hash

# Generate hash untuk password baru
new_password = "newpassword123"
password_hash = generate_password_hash(new_password)
print(f"Hash: {password_hash}")
```

### **Via Flask Shell**
```bash
# Masuk ke Flask shell
flask shell

# Generate hash
from werkzeug.security import generate_password_hash
hash = generate_password_hash("newpassword123")
print(hash)
```

## 🚨 **Security Best Practices**

### **1. Jangan Simpan Password Plain Text**
```python
# ❌ SALAH - Jangan lakukan ini
user.password = "plaintext_password"

# ✅ BENAR - Selalu hash password
user.set_password("plaintext_password")
```

### **2. Gunakan Password yang Kuat**
```python
# Contoh password yang baik
good_passwords = [
    "MySecure123!",
    "P@ssw0rd2024",
    "Admin#123",
    "User$456"
]

# Contoh password yang buruk
bad_passwords = [
    "123456",
    "password",
    "admin",
    "qwerty"
]
```

### **3. Validasi Password**
```python
def validate_password(password):
    """Validasi kekuatan password"""
    if len(password) < 8:
        return False, "Password minimal 8 karakter"
    
    if not any(c.isupper() for c in password):
        return False, "Password harus ada huruf besar"
    
    if not any(c.islower() for c in password):
        return False, "Password harus ada huruf kecil"
    
    if not any(c.isdigit() for c in password):
        return False, "Password harus ada angka"
    
    return True, "Password valid"
```

## 🔍 **Troubleshooting**

### **Problem: User tidak bisa login**
```python
# 1. Cek apakah user ada
user = User.query.filter_by(email='user@example.com').first()
if not user:
    print("User tidak ditemukan")

# 2. Test password
if user.check_password("input_password"):
    print("Password benar")
else:
    print("Password salah")

# 3. Reset password
user.set_password("new_password")
db.session.commit()
```

### **Problem: Hash tidak valid**
```python
# Cek format hash
hash_pattern = r'^pbkdf2:sha256:\d+:\$[a-zA-Z0-9]+\$[a-zA-Z0-9+/=]+$'
import re

if re.match(hash_pattern, user.password_hash):
    print("Hash format valid")
else:
    print("Hash format tidak valid - perlu reset")
```

## 📋 **Quick Commands**

### **Reset Password User**
```bash
# Via admin tool
python admin_reset_password.py

# Via Flask shell
flask shell
>>> user = User.query.filter_by(email='user@example.com').first()
>>> user.set_password('newpassword123')
>>> db.session.commit()
```

### **Buat User Baru**
```bash
# Via password utils
python password_utils.py

# Via Flask shell
flask shell
>>> user = User(name='New User', email='new@example.com')
>>> user.set_password('password123')
>>> db.session.add(user)
>>> db.session.commit()
```

### **List Semua User**
```bash
# Via admin tool
python admin_reset_password.py

# Via Flask shell
flask shell
>>> users = User.query.all()
>>> for u in users: print(f"{u.email}: {u.password_hash}")
```

## ⚠️ **Peringatan Keamanan**

1. **Jangan pernah** mencoba reverse hash password
2. **Selalu** gunakan reset password untuk "lupa password"
3. **Jangan** simpan password di log atau file
4. **Gunakan** HTTPS untuk transmisi password
5. **Validasi** kekuatan password saat registrasi

## 🔗 **Referensi**

- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.3.x/utils/#werkzeug.security)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Flask Security](https://flask-security-too.readthedocs.io/)
