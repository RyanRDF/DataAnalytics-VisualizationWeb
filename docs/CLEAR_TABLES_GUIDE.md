# 🧹 Panduan Clear Tabel - DAV Project

## 🛠️ **Tool untuk Clear Semua Tabel**

### **Jalankan Tool**
```bash
python clear_all_tables.py
```

## 📋 **Menu Options**

### **1. Lihat Jumlah Data di Setiap Tabel**
- Tampilkan count records di semua tabel
- Status tabel (kosong/berisi)
- Total records keseluruhan

### **2. Clear Tabel Tertentu**
- Pilih tabel yang ingin di-clear
- Konfirmasi sebelum menghapus
- Safe untuk testing

### **3. Clear Semua Tabel Rumah Sakit**
- Hapus data hospital tables saja
- Tetap pertahankan user system
- Urutan FK yang benar

### **4. Clear Semua Tabel Sistem**
- Hapus user, session, upload log
- Tetap pertahankan data hospital
- Untuk reset user system

### **5. Clear SEMUA Tabel (HATI-HATI!)**
- Hapus semua data di semua tabel
- Urutan FK yang benar
- Konfirmasi ganda

## 🔧 **Fungsi yang Tersedia**

### **clear_all_tables()**
```python
def clear_all_tables():
    """Clear semua isi tabel dengan aman (urutan yang benar untuk FK)"""
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
```

### **clear_specific_table()**
```python
def clear_specific_table():
    """Clear tabel tertentu saja"""
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
```

### **show_table_counts()**
```python
def show_table_counts():
    """Tampilkan jumlah data di setiap tabel"""
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
```

## 🚨 **Urutan Penghapusan (Penting!)**

### **Mengapa Urutan Penting?**
Foreign key constraints memerlukan urutan penghapusan yang benar:

```python
# ❌ SALAH - Akan error FK constraint
# Hapus User dulu, padahal UserSession masih reference ke User

# ✅ BENAR - Urutan yang benar
1. KunjunganDiagnosa (FK ke Kunjungan, Diagnosa)
2. KunjunganProsedur (FK ke Kunjungan, Prosedur)
3. RincianBiaya (FK ke Kunjungan)
4. Kunjungan (FK ke Pasien, Dokter)
5. UserSession (FK ke User)
6. DataUploadLog (FK ke User)
7. Pasien (Master table)
8. Dokter (Master table)
9. Diagnosa (Master table)
10. Prosedur (Master table)
11. User (Master table)
```

## 📊 **Contoh Penggunaan**

### **Scenario 1: Clear Semua Data untuk Testing**
```bash
python clear_all_tables.py
# Pilih menu 5 (Clear SEMUA tabel)
# Konfirmasi: CLEAR ALL
```

### **Scenario 2: Clear Hanya Data Hospital**
```bash
python clear_all_tables.py
# Pilih menu 3 (Clear semua tabel rumah sakit)
# Konfirmasi: CLEAR HOSPITAL
```

### **Scenario 3: Clear Hanya User System**
```bash
python clear_all_tables.py
# Pilih menu 4 (Clear semua tabel sistem)
# Konfirmasi: CLEAR SYSTEM
```

### **Scenario 4: Clear Tabel Tertentu**
```bash
python clear_all_tables.py
# Pilih menu 2 (Clear tabel tertentu)
# Pilih nomor tabel (misal: 8 untuk Kunjungan)
# Konfirmasi: y
```

## 🔍 **Manual via Flask Shell**

### **Clear Semua Tabel**
```bash
flask shell
```

```python
from src.core.database import db, User, UserSession, DataUploadLog, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur

# Urutan yang benar
KunjunganDiagnosa.query.delete()
KunjunganProsedur.query.delete()
RincianBiaya.query.delete()
Kunjungan.query.delete()
UserSession.query.delete()
DataUploadLog.query.delete()
Pasien.query.delete()
Dokter.query.delete()
Diagnosa.query.delete()
Prosedur.query.delete()
User.query.delete()

db.session.commit()
print("Semua tabel berhasil di-clear!")
```

### **Clear Tabel Tertentu**
```python
# Clear hanya tabel Kunjungan
Kunjungan.query.delete()
db.session.commit()
print("Tabel Kunjungan berhasil di-clear!")
```

### **Cek Jumlah Data**
```python
# Cek jumlah data di setiap tabel
tables = [User, UserSession, DataUploadLog, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur]

for table in tables:
    count = table.query.count()
    print(f"{table.__name__}: {count} records")
```

## 🚨 **Peringatan Penting**

### **1. Backup Data**
```bash
# Backup database sebelum clear
pg_dump -U postgres DAV > backup_before_clear_$(date +%Y%m%d_%H%M%S).sql
```

### **2. Test di Development**
- Selalu test di environment development dulu
- Jangan langsung clear di production

### **3. Konfirmasi Ganda**
- Tool memerlukan konfirmasi yang spesifik
- Ketik persis seperti yang diminta

### **4. Monitor Aplikasi**
- Cek aplikasi setelah clear
- Pastikan tidak ada error

## 🔧 **Troubleshooting**

### **Problem: FK Constraint Error**
```python
# Jika masih error, cek urutan penghapusan
# Pastikan tabel dengan FK dihapus dulu

# Cek FK constraints
from sqlalchemy import inspect
inspector = inspect(db.engine)

for table_name in inspector.get_table_names():
    fks = inspector.get_foreign_keys(table_name)
    if fks:
        print(f"{table_name}: {fks}")
```

### **Problem: Data Masih Ada**
```python
# Cek apakah masih ada data
for table in [User, UserSession, DataUploadLog, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur]:
    count = table.query.count()
    if count > 0:
        print(f"{table.__name__}: {count} records masih ada")
```

### **Problem: Error Saat Commit**
```python
try:
    db.session.commit()
    print("✅ Berhasil!")
except Exception as e:
    print(f"❌ Error: {e}")
    db.session.rollback()
```

## 📋 **Quick Commands**

### **Clear Semua Tabel**
```bash
python clear_all_tables.py
# Menu 5 → CLEAR ALL
```

### **Clear Hospital Tables**
```bash
python clear_all_tables.py
# Menu 3 → CLEAR HOSPITAL
```

### **Clear System Tables**
```bash
python clear_all_tables.py
# Menu 4 → CLEAR SYSTEM
```

### **Cek Jumlah Data**
```bash
python clear_all_tables.py
# Menu 1
```

## 🎯 **Best Practices**

1. **Selalu backup** sebelum clear
2. **Test di development** dulu
3. **Gunakan urutan yang benar** untuk FK
4. **Konfirmasi ganda** sebelum menghapus
5. **Monitor aplikasi** setelah clear
6. **Document** perubahan yang dilakukan

## 🔗 **Related Tools**

- `delete_user_tool.py` - Hapus user tertentu
- `admin_reset_password.py` - Reset password user
- `run_migration.py` - Setup database
- `password_utils.py` - Manage password
