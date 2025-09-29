# 🗑️ Panduan Menghapus User - DAV Project

## ⚠️ **Error Foreign Key Constraint**

Error yang Anda alami:
```
ERROR: update or delete on table "users" violates foreign key constraint 
"user_sessions_user_id_fkey" on table "user_sessions"
DETAIL: Key (id)=(4) is still referenced from table "user_sessions".
```

**Penyebab:** User tidak bisa dihapus karena masih ada session aktif yang mereferensikan user tersebut.

## 🛠️ **Solusi: Hapus User dengan Aman**

### **1. Gunakan Delete User Tool (Recommended)**
```bash
python delete_user_tool.py
```

Tool ini akan:
- ✅ Hapus semua session user
- ✅ Hapus semua upload log user  
- ✅ Hapus user
- ✅ Handle foreign key constraint

### **2. Manual via Database**
```sql
-- 1. Hapus sessions terlebih dahulu
DELETE FROM user_sessions WHERE user_id = 4;

-- 2. Hapus upload logs
DELETE FROM data_upload_logs WHERE user_id = 4;

-- 3. Baru hapus user
DELETE FROM users WHERE id = 4;
```

### **3. Via Flask Shell**
```bash
flask shell
```

```python
# Import models
from src.core.database import db, User, UserSession, DataUploadLog

# Cari user
user = User.query.get(4)  # Ganti dengan ID user yang ingin dihapus

# Hapus sessions
sessions = UserSession.query.filter_by(user_id=user.id).all()
for session in sessions:
    db.session.delete(session)

# Hapus upload logs
uploads = DataUploadLog.query.filter_by(user_id=user.id).all()
for upload in uploads:
    db.session.delete(upload)

# Hapus user
db.session.delete(user)

# Commit
db.session.commit()
print("User berhasil dihapus!")
```

## 🔧 **Delete User Tool Features**

### **Menu Options:**
1. **List semua user** - Lihat semua user dengan detail
2. **Hapus user by ID** - Hapus berdasarkan ID
3. **Hapus user by Email** - Hapus berdasarkan email
4. **Cleanup expired sessions** - Bersihkan session yang sudah expired
5. **Keluar**

### **Safety Features:**
- ✅ Konfirmasi ganda (ketik 'DELETE')
- ✅ Tampilkan data yang akan dihapus
- ✅ Rollback jika error
- ✅ Hapus data terkait secara otomatis

## 📋 **Contoh Penggunaan**

### **Scenario 1: Hapus User dengan ID 4**
```bash
python delete_user_tool.py
# Pilih menu 2 (Hapus user by ID)
# Masukkan ID: 4
# Konfirmasi: DELETE
```

### **Scenario 2: Hapus User dengan Email**
```bash
python delete_user_tool.py
# Pilih menu 3 (Hapus user by Email)
# Masukkan email: user@example.com
# Konfirmasi: DELETE
```

### **Scenario 3: List User untuk Cek Data**
```bash
python delete_user_tool.py
# Pilih menu 1 (List semua user)
# Lihat detail user sebelum menghapus
```

## 🔍 **Troubleshooting**

### **Problem: User masih tidak bisa dihapus**
```python
# Cek apakah masih ada referensi
from src.core.database import db, User, UserSession, DataUploadLog

user_id = 4
sessions = UserSession.query.filter_by(user_id=user_id).count()
uploads = DataUploadLog.query.filter_by(user_id=user_id).count()

print(f"Sessions: {sessions}")
print(f"Uploads: {uploads}")

# Jika masih ada, hapus manual
if sessions > 0:
    UserSession.query.filter_by(user_id=user_id).delete()
if uploads > 0:
    DataUploadLog.query.filter_by(user_id=user_id).delete()

db.session.commit()
```

### **Problem: Error saat commit**
```python
try:
    db.session.commit()
    print("✅ Berhasil!")
except Exception as e:
    print(f"❌ Error: {e}")
    db.session.rollback()
```

## 🚨 **Peringatan Penting**

1. **Backup data** sebelum menghapus user
2. **Hapus data terkait** terlebih dahulu
3. **Konfirmasi** sebelum menghapus
4. **Test** di environment development dulu
5. **Monitor** aplikasi setelah penghapusan

## 🔗 **Related Commands**

### **Cek User dan Data Terkait**
```sql
-- Cek user
SELECT * FROM users WHERE id = 4;

-- Cek sessions
SELECT * FROM user_sessions WHERE user_id = 4;

-- Cek upload logs
SELECT * FROM data_upload_logs WHERE user_id = 4;
```

### **Hapus Session Expired**
```sql
-- Hapus session yang sudah expired
DELETE FROM user_sessions 
WHERE expires_at < NOW();
```

### **Reset User (Alternatif ke Delete)**
```bash
# Jika tidak ingin menghapus, bisa reset password
python admin_reset_password.py
```

## 📊 **Database Schema Reference**

```sql
-- Tabel users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Tabel user_sessions (Foreign Key ke users)
CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id), -- FK constraint
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabel data_upload_logs (Foreign Key ke users)
CREATE TABLE data_upload_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id), -- FK constraint
    filename VARCHAR(255) NOT NULL,
    file_size INTEGER,
    rows_processed INTEGER,
    upload_time TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'success',
    error_message TEXT
);
```

## 🎯 **Best Practices**

1. **Gunakan tool** yang sudah disediakan
2. **Backup database** sebelum operasi bulk
3. **Test** di environment development
4. **Monitor** aplikasi setelah perubahan
5. **Document** perubahan yang dilakukan
