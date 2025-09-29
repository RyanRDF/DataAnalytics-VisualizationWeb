# Hospital Database Schema - DAV Project

## Overview

Database schema untuk analisis data rumah sakit yang terintegrasi dengan sistem Data Analytics Visualization (DAV) yang sudah ada.

## 🏗️ Database Structure

### Tabel Master (Referensi)
- **`pasien`** - Data unik pasien dengan MRN sebagai primary key
- **`dokter`** - Data dokter dengan ID auto-increment  
- **`diagnosa`** - Lookup kode diagnosa ICD-10
- **`prosedur`** - Lookup kode prosedur ICD-9CM

### Tabel Transaksi
- **`kunjungan`** - Tabel utama untuk setiap kunjungan/rawat inap
- **`rincian_biaya`** - Detail biaya per kunjungan (One-to-One)

### Tabel Penghubung (Many-to-Many)
- **`kunjungan_diagnosa`** - Menghubungkan kunjungan dengan diagnosa
- **`kunjungan_prosedur`** - Menghubungkan kunjungan dengan prosedur

### Tabel Sistem (Existing)
- **`users`** - Data pengguna sistem
- **`user_sessions`** - Session management
- **`data_upload_logs`** - Log upload data

## 🚀 Installation & Setup

### 1. Prerequisites
- PostgreSQL 12+ 
- Python 3.8+
- Dependencies: `psycopg2-binary`, `flask-sqlalchemy`, `flask-migrate`

### 2. Database Setup
```bash
# 1. Pastikan PostgreSQL berjalan
sudo systemctl start postgresql

# 2. Buat database DAV (jika belum ada)
createdb -U postgres DAV

# 3. Jalankan migrasi
python run_migration.py
```

### 3. Flask Integration
```python
# Import models di aplikasi Flask
from src.core.database import db, Pasien, Dokter, Kunjungan, RincianBiaya

# Models sudah terintegrasi dengan SQLAlchemy
# Gunakan Flask-Migrate untuk sync schema
flask db migrate -m "Add hospital tables"
flask db upgrade
```

## 📊 ERD Diagram

Lihat file `hospital_erd.md` untuk ERD diagram lengkap dengan Mermaid.

## 🔧 Usage Examples

### Insert Data Pasien
```python
from src.core.database import db, Pasien

# Buat pasien baru
pasien = Pasien(
    mrn='MRN001',
    nama_pasien='John Doe',
    birth_date='1980-01-15',
    sex=1,  # 1=Laki-laki, 2=Perempuan
    no_kartu_bpjs='BPJS001',
    umur_tahun=44
)

db.session.add(pasien)
db.session.commit()
```

### Insert Data Kunjungan
```python
from src.core.database import db, Kunjungan, RincianBiaya

# Buat kunjungan
kunjungan = Kunjungan(
    mrn='MRN001',
    dokter_id=1,
    admission_date='2024-01-15',
    discharge_date='2024-01-20',
    los=5,
    kelas_rawat=2,
    total_tarif=5000000,
    tarif_rs=4500000
)

db.session.add(kunjungan)
db.session.commit()

# Buat rincian biaya
rincian = RincianBiaya(
    kunjungan_id=kunjungan.kunjungan_id,
    prosedur_non_bedah=1000000,
    prosedur_bedah=2000000,
    konsultasi=500000,
    obat=1500000
)

db.session.add(rincian)
db.session.commit()
```

### Query dengan Join
```python
from src.core.database import db, Kunjungan, Pasien, Dokter

# Query kunjungan dengan data pasien dan dokter
kunjungan_data = db.session.query(Kunjungan)\
    .join(Pasien, Kunjungan.mrn == Pasien.mrn)\
    .join(Dokter, Kunjungan.dokter_id == Dokter.dokter_id)\
    .filter(Kunjungan.admission_date >= '2024-01-01')\
    .all()

for kunjungan in kunjungan_data:
    print(f"Pasien: {kunjungan.pasien.nama_pasien}")
    print(f"Dokter: {kunjungan.dokter.nama_dokter}")
    print(f"Tanggal Masuk: {kunjungan.admission_date}")
    print(f"LOS: {kunjungan.los} hari")
```

## 📈 Analytics Integration

Database ini dirancang untuk mendukung analisis yang sudah ada di handlers:

### Financial Analysis
```python
# Query untuk analisis keuangan
financial_data = db.session.query(
    Kunjungan.kode_inacbg,
    db.func.sum(Kunjungan.total_tarif).label('total_biaya'),
    db.func.avg(Kunjungan.total_tarif).label('rata_biaya'),
    db.func.count(Kunjungan.kunjungan_id).label('jumlah_kunjungan')
).group_by(Kunjungan.kode_inacbg).all()
```

### Length of Stay Analysis
```python
# Query untuk analisis LOS
los_data = db.session.query(
    Kunjungan.kode_inacbg,
    db.func.avg(Kunjungan.los).label('rata_los'),
    db.func.min(Kunjungan.los).label('min_los'),
    db.func.max(Kunjungan.los).label('max_los')
).group_by(Kunjungan.kode_inacbg).all()
```

### Patient Analysis
```python
# Query untuk analisis pasien
patient_data = db.session.query(
    Pasien.sex,
    db.func.count(Kunjungan.kunjungan_id).label('jumlah_kunjungan'),
    db.func.avg(Kunjungan.los).label('rata_los')
).join(Kunjungan, Pasien.mrn == Kunjungan.mrn)\
.group_by(Pasien.sex).all()
```

## 🔍 Indexes & Performance

Database sudah dioptimasi dengan indeks pada:
- `kunjungan.mrn` - Untuk join dengan pasien
- `kunjungan.admission_date` - Untuk filter tanggal
- `kunjungan.discharge_date` - Untuk analisis periode
- `kunjungan.kode_inacbg` - Untuk analisis INA-CBG
- `pasien.no_kartu_bpjs` - Untuk lookup BPJS

## 🛠️ Maintenance

### Backup Database
```bash
pg_dump -U postgres DAV > backup_dav_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql -U postgres DAV < backup_dav_20240115.sql
```

### Update Schema
```bash
# Setelah mengubah models SQLAlchemy
flask db migrate -m "Update hospital schema"
flask db upgrade
```

## 📋 Sample Data

Script migrasi sudah menyertakan sample data untuk testing:
- 3 pasien sample
- 3 dokter sample  
- 5 diagnosa ICD-10 sample
- 5 prosedur ICD-9CM sample

## 🔗 Integration dengan Handlers

Database ini kompatibel dengan handlers yang sudah ada:
- `financial_handler.py` - Analisis keuangan
- `patient_handler.py` - Analisis pasien
- `los_handler.py` - Analisis Length of Stay
- `inacbg_handler.py` - Analisis INA-CBG
- `ventilator_handler.py` - Analisis ventilator
- `selisih_tarif_handler.py` - Analisis selisih tarif

## 📞 Support

Untuk pertanyaan atau masalah:
1. Cek log error di aplikasi Flask
2. Verifikasi koneksi database
3. Pastikan semua dependencies terinstall
4. Cek konfigurasi database di `src/core/database.py`
