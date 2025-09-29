# ERD Database Rumah Sakit - Data Analytics Visualization (DAV)

## Entity Relationship Diagram

```mermaid
erDiagram
    %% Tabel Master (Referensi)
    Pasien {
        string mrn PK "Medical Record Number"
        string nama_pasien "Nama Lengkap Pasien"
        date birth_date "Tanggal Lahir"
        smallint sex "1=Laki-laki, 2=Perempuan"
        string no_kartu_bpjs UK "Nomor Kartu BPJS"
        integer umur_tahun "Umur dalam Tahun"
        integer umur_hari "Umur dalam Hari"
    }
    
    Dokter {
        integer dokter_id PK "ID Dokter (Auto-increment)"
        string nama_dokter "Nama Lengkap Dokter"
    }
    
    Diagnosa {
        string kode_diagnosa PK "Kode ICD-10"
        text deskripsi "Deskripsi Diagnosa"
    }
    
    Prosedur {
        string kode_prosedur PK "Kode ICD-9CM"
        text deskripsi "Deskripsi Prosedur"
    }
    
    %% Tabel Transaksi
    Kunjungan {
        integer kunjungan_id PK "ID Kunjungan (Auto-increment)"
        string mrn FK "Medical Record Number"
        integer dokter_id FK "ID Dokter"
        date admission_date "Tanggal Masuk"
        date discharge_date "Tanggal Keluar"
        integer los "Length of Stay (hari)"
        smallint kelas_rawat "Kelas Rawat (1,2,3)"
        string discharge_status "Status Keluar"
        string kode_inacbg "Kode INA-CBG"
        string sep "Surat Eligibilitas Peserta"
        bigint total_tarif "Total Tarif"
        bigint tarif_rs "Tarif Rumah Sakit"
    }
    
    RincianBiaya {
        integer rincian_id PK "ID Rincian (Auto-increment)"
        integer kunjungan_id FK UK "ID Kunjungan (One-to-One)"
        bigint prosedur_non_bedah "Biaya Prosedur Non-Bedah"
        bigint prosedur_bedah "Biaya Prosedur Bedah"
        bigint konsultasi "Biaya Konsultasi"
        bigint tenaga_ahli "Biaya Tenaga Ahli"
        bigint keperawatan "Biaya Keperawatan"
        bigint penunjang "Biaya Penunjang"
        bigint radiologi "Biaya Radiologi"
        bigint laboratorium "Biaya Laboratorium"
        bigint pelayanan_darah "Biaya Pelayanan Darah"
        bigint kamar_akomodasi "Biaya Kamar & Akomodasi"
        bigint obat "Biaya Obat"
    }
    
    %% Tabel Penghubung (Many-to-Many)
    KunjunganDiagnosa {
        integer kunjungan_id PK,FK "ID Kunjungan"
        string kode_diagnosa PK,FK "Kode Diagnosa"
    }
    
    KunjunganProsedur {
        integer kunjungan_id PK,FK "ID Kunjungan"
        string kode_prosedur PK,FK "Kode Prosedur"
    }
    
    %% Tabel Sistem (Existing)
    User {
        integer id PK "User ID"
        string name "Nama User"
        string email UK "Email User"
        string password_hash "Hash Password"
        boolean is_active "Status Aktif"
        datetime created_at "Tanggal Dibuat"
        datetime last_login "Login Terakhir"
    }
    
    UserSession {
        integer id PK "Session ID"
        integer user_id FK "User ID"
        string session_token UK "Token Session"
        datetime created_at "Tanggal Dibuat"
        datetime expires_at "Tanggal Expired"
        boolean is_active "Status Aktif"
    }
    
    DataUploadLog {
        integer id PK "Log ID"
        integer user_id FK "User ID"
        string filename "Nama File"
        integer file_size "Ukuran File"
        integer rows_processed "Jumlah Baris Diproses"
        datetime upload_time "Waktu Upload"
        string status "Status Upload"
        text error_message "Pesan Error"
    }
    
    %% Relationships
    Pasien ||--o{ Kunjungan : "memiliki"
    Dokter ||--o{ Kunjungan : "menangani"
    Kunjungan ||--|| RincianBiaya : "memiliki"
    Kunjungan ||--o{ KunjunganDiagnosa : "memiliki"
    Kunjungan ||--o{ KunjunganProsedur : "memiliki"
    Diagnosa ||--o{ KunjunganDiagnosa : "terkait"
    Prosedur ||--o{ KunjunganProsedur : "terkait"
    
    %% Sistem relationships
    User ||--o{ UserSession : "memiliki"
    User ||--o{ DataUploadLog : "mengupload"
```

## Deskripsi Relasi

### 1. Tabel Master (Referensi)
- **Pasien**: Data unik pasien dengan MRN sebagai primary key
- **Dokter**: Data dokter dengan ID auto-increment
- **Diagnosa**: Lookup kode diagnosa ICD-10
- **Prosedur**: Lookup kode prosedur ICD-9CM

### 2. Tabel Transaksi
- **Kunjungan**: Tabel utama untuk setiap kunjungan/rawat inap
- **RincianBiaya**: Detail biaya per kunjungan (One-to-One)

### 3. Tabel Penghubung (Many-to-Many)
- **KunjunganDiagnosa**: Menghubungkan kunjungan dengan diagnosa
- **KunjunganProsedur**: Menghubungkan kunjungan dengan prosedur

### 4. Tabel Sistem (Existing)
- **User**: Data pengguna sistem
- **UserSession**: Session management
- **DataUploadLog**: Log upload data

## Karakteristik Database

### Constraints
- Foreign Key constraints untuk integritas referensial
- Unique constraints untuk data unik (MRN, email, session_token)
- Cascade delete untuk data terkait

### Indeks
- Indeks pada kolom yang sering di-query (mrn, admission_date)
- Indeks pada foreign key untuk performa join

### Tipe Data
- **BIGINT**: Untuk nilai biaya yang besar
- **SMALLINT**: Untuk kode kategori (sex, kelas_rawat)
- **DATE**: Untuk tanggal
- **TEXT**: Untuk deskripsi panjang
- **VARCHAR**: Untuk string dengan panjang terbatas

## Kompatibilitas dengan Sistem Existing

Database ini dirancang untuk:
1. **Kompatibel** dengan tabel sistem existing (User, UserSession, DataUploadLog)
2. **Mendukung** analisis data rumah sakit yang sudah ada di handlers
3. **Menggunakan** konfigurasi database yang sama (PostgreSQL DAV)
4. **Mengikuti** pola naming convention yang konsisten
