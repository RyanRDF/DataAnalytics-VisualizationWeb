# Sistem Upload Baru

## Overview
Sistem upload telah diubah untuk mengikuti alur yang lebih terstruktur sesuai permintaan user:

1. **User Input File** - User mengupload file
2. **File di analisa txt/xlsx** - Sistem menganalisa tipe file
3. **Ekstraksi data dengan funsinya masing masing txt & xlsx** - Data diekstrak sesuai tipe file
4. **Masukkan ke dataframe (menggunakan pandas df)** - Data dimasukkan ke DataFrame pandas
5. **Verifikasi dataframe yang ingin dikirim dengan isi tabel yang sudah ada menggunakan SEP** - Cek duplikasi berdasarkan SEP
6. **Kirim data yang valid dan jangan kirim data yang duplikat** - Hanya data valid yang diupload
7. **Informasi rows_success dan row_failednya di kirim juga ke tabel upload logs** - Logging ke database
8. **Tampilkan informasi di data status** - Menampilkan hasil di UI
9. **Empty dataframenya setelah sukses mengirim data** - Bersihkan DataFrame untuk upload berikutnya

## Komponen Baru

### 1. FileAnalyzer (`src/core/file_analyzer.py`)
- Menganalisa tipe file (txt/xlsx)
- Mendeteksi encoding untuk file text
- Memvalidasi file yang didukung

### 2. DataExtractor (`src/core/data_extractor.py`)
- Mengekstrak data dari file txt dan xlsx
- Menggunakan pandas untuk memproses data
- Membersihkan DataFrame dari data kosong

### 3. DataFrameManager (`src/core/dataframe_manager.py`)
- Mengelola DataFrame pandas
- Memisahkan data valid dan duplikat
- Membersihkan DataFrame setelah upload

### 4. DuplicateChecker (`src/core/duplicate_checker.py`)
- Mengecek duplikasi berdasarkan SEP
- Mengambil SEP yang sudah ada di database
- Memisahkan data baru dan duplikat

### 5. UploadService (`src/core/upload_service.py`)
- Menggabungkan semua komponen
- Mengelola alur upload yang terstruktur
- Menangani logging ke database

## Perubahan pada File Existing

### 1. Routes (`src/web/routes.py`)
- Menggunakan UploadService yang baru
- Menghapus logika upload manual
- Menyederhanakan fungsi upload_file

### 2. JavaScript (`src/web/static/script.js`)
- Update fungsi `updateDataStatusAfterUpload`
- Menampilkan rows_success dan rows_failed
- Menggunakan struktur data yang baru

### 3. Requirements (`requirements.txt`)
- Menambahkan `chardet` untuk deteksi encoding

## Alur Upload Baru

```
User Upload File
       ↓
FileAnalyzer.analyze_file()
       ↓
DataExtractor.extract_data()
       ↓
DataFrameManager.set_dataframe()
       ↓
DataFrameManager.validate_dataframe()
       ↓
DuplicateChecker.check_duplicates()
       ↓
DataFrameManager.separate_valid_duplicate_data()
       ↓
UploadService._upload_valid_data()
       ↓
UploadService._log_upload()
       ↓
DataFrameManager.clear_dataframe()
       ↓
Update UI dengan hasil
```

## Fitur Baru

1. **Deteksi Encoding Otomatis** - Untuk file text dengan encoding yang berbeda
2. **Pemisahan Data Valid/Duplikat** - Berdasarkan SEP yang sudah ada
3. **Logging Terstruktur** - Menyimpan rows_success dan rows_failed
4. **UI Feedback** - Menampilkan informasi upload yang jelas
5. **DataFrame Management** - Otomatis membersihkan DataFrame setelah upload

## Testing

Untuk test sistem baru:

1. Upload file `P.04092025_data_ujicoba_apps_analisa.txt` untuk pertama kali
2. Upload file yang sama untuk kedua kalinya (test duplicate detection)
3. Verifikasi Data Status menampilkan "Rows Failed: 18" dan "Rows Success: 0"
4. Test dengan file Excel (.xlsx)
5. Test dengan file text dengan encoding berbeda

## Database Schema

UploadLog table sudah memiliki kolom:
- `rows_success` - Jumlah baris yang berhasil diupload
- `rows_failed` - Jumlah baris yang gagal (duplikat)
- `rows_processed` - Total baris yang diproses

## Error Handling

Sistem baru memiliki error handling yang lebih baik:
- Validasi file sebelum ekstraksi
- Error handling untuk setiap step
- Rollback database jika ada error
- Logging error yang detail

