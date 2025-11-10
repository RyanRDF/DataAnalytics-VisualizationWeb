# 📊 Struktur Database

## Overview
Sistem menggunakan struktur database yang sederhana dengan fokus pada tabel `data_analytics` sebagai single source of truth untuk semua data.

## ✅ Tabel Aktif (7 Tabel)

### 1. **data_analytics** (Tabel Utama)
Tabel utama yang menyimpan semua data medis dan keuangan.
- **Info pasien**: `nama_pasien`, `mrn`, `birth_date`, `sex`
- **Info kunjungan**: `sep`, `admission_date`, `discharge_date`, `los`
- **Info medis**: `diaglist`, `proclist`, `inacbg`, `dpjp`
- **Info keuangan**: `total_tarif`, `tarif_rs`, dan rincian biaya lengkap
- **Data ICU/Ventilator**: `icu_indikator`, `icu_los`, `vent_hour`

### 2. **users**
Management user dan authentication dengan kolom `role` untuk role management.

### 3. **user_sessions**
Session management untuk track login user.

### 4. **upload_logs**
Tracking file upload dengan detail status dan hasil processing.

### 5. **login_logs**
Tracking semua aktivitas login (success, failed, blocked).

### 6. **user_activity_logs**
Log semua aktivitas user dalam sistem.

<!-- registration_codes dihapus dari desain normalisasi -->

## ❌ Tabel Yang Dihapus

Tabel-tabel berikut telah dihapus karena tidak digunakan:
- Tabel hospital lama (Pasien, Dokter, Diagnosa, Kunjungan, dll)
- Tabel role management (UserRole, UserRoleAssignment)
- **Alasan**: Data sudah ada di `data_analytics` dan tidak memerlukan tabel terpisah

## 🔄 Data Flow

```
File Upload → RobustDataExtractor → data_analytics Table
                ↓
         DatabaseQueryService → Handlers → Display
```

## 📈 Benefits

1. **Simple**: Hanya 7 tabel yang mudah dipahami
2. **Fast**: Tidak perlu join multiple tables
3. **Maintainable**: Struktur jelas dan konsisten
4. **Scalable**: Mudah untuk maintenance dan update

---

*Struktur ini hasil dari simplification untuk fokus pada analytics*
