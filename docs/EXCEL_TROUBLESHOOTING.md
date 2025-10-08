# 🔧 Panduan Troubleshooting Upload File Excel

## Masalah yang Sering Terjadi

### 1. File Excel Tidak Terdeteksi Kolom
**Gejala:** Sistem tidak bisa mendeteksi kolom atau jumlah baris dari file Excel

**Penyebab:**
- Format Excel tidak standar
- Ada baris kosong di awal file
- Encoding masalah
- Engine pandas tidak kompatibel

**Solusi:**
1. **Gunakan script debugging:**
   ```bash
   python debug_excel_upload.py "nama_file.xlsx"
   ```

2. **Gunakan script testing:**
   ```bash
   python test_excel_file.py "nama_file.xlsx"
   ```

3. **Perbaiki file Excel:**
   - Buka file di Excel
   - Pastikan header ada di baris pertama
   - Hapus baris kosong di awal
   - Simpan ulang sebagai .xlsx

### 2. Kolom Tidak Ditemukan
**Gejala:** Error "Missing required columns"

**Penyebab:**
- Nama kolom tidak sama persis
- Ada spasi ekstra di nama kolom
- Kolom menggunakan nama yang berbeda

**Solusi:**
1. **Periksa nama kolom yang diperlukan:**
   ```
   KODE_RS, KELAS_RS, KELAS_RAWAT, KODE_TARIF,
   ADMISSION_DATE, DISCHARGE_DATE, BIRTH_DATE, SEX,
   NAMA_PASIEN, MRN, DPJP, TOTAL_TARIF, TARIF_RS,
   LOS, KODE_INACBG, SEP
   ```

2. **Pastikan nama kolom sama persis** (case-sensitive)

3. **Hapus spasi ekstra** di nama kolom

### 3. Data Kosong atau Null
**Gejala:** Error "Column contains null values"

**Penyebab:**
- Ada sel kosong di kolom wajib
- Format data tidak sesuai

**Solusi:**
1. **Isi semua sel wajib** (MRN, NAMA_PASIEN, ADMISSION_DATE)
2. **Gunakan format yang benar:**
   - Tanggal: DD/MM/YYYY atau YYYY-MM-DD
   - Jenis kelamin: 1 atau 2
   - Numerik: angka tanpa format khusus

## Langkah-langkah Debugging

### 1. Jalankan Script Debugging
```bash
cd DataAnalytics-VisualizationWeb
python debug_excel_upload.py "P.04092025 data ujicoba apps analisa.xlsx"
```

### 2. Jalankan Script Testing
```bash
python test_excel_file.py "P.04092025 data ujicoba apps analisa.xlsx"
```

### 3. Periksa Log Aplikasi
Saat upload, periksa console/log untuk pesan debugging:
```
📊 File read successfully:
  - File: /path/to/file.xlsx
  - Rows: 100
  - Columns: 15
  - Column names: ['KODE_RS', 'KELAS_RS', ...]

🔍 Validating data:
  - Total rows: 100
  - Total columns: 15
  - Found columns: ['KODE_RS', 'KELAS_RS', ...]
  ✅ All required columns found
```

## Template Excel yang Benar

### Format Header (Baris 1):
```
KODE_RS | KELAS_RS | KELAS_RAWAT | KODE_TARIF | ADMISSION_DATE | DISCHARGE_DATE | BIRTH_DATE | SEX | NAMA_PASIEN | MRN | DPJP | TOTAL_TARIF | TARIF_RS | LOS | KODE_INACBG | SEP
```

### Format Data (Baris 2+):
```
RS001 | 1 | 1 | T001 | 15/01/2024 | 20/01/2024 | 01/01/1980 | 1 | John Doe | MRN001 | Dr. Smith | 1000000 | 800000 | 5 | INA001 | SEP001
```

## Perbaikan yang Sudah Dilakukan

### 1. Enhanced Excel Reading
- Multiple engine support (openpyxl, xlrd)
- Better error handling
- Fallback methods

### 2. Detailed Logging
- File reading status
- Column detection
- Validation results

### 3. Better Error Messages
- Specific error descriptions
- Column names in error messages
- Row count information

## Cara Menggunakan Script Debugging

### 1. Debug Script
```bash
python debug_excel_upload.py "file.xlsx"
```

**Output yang diharapkan:**
```
🔍 LAPORAN DEBUGGING FILE EXCEL
============================================================

📁 INFORMASI FILE:
  - File ada: ✅
  - Ukuran file: 15,234 bytes
  - Ekstensi: .xlsx

📊 STATUS PEMBACAAN:
  - Pandas berhasil: ✅
  - Baris data: 100
  - Kolom data: 15

📋 ANALISIS KOLOM:
  - Kolom yang ditemukan: 15
  - Kolom yang diperlukan: 15
  - Kolom yang hilang: 0
```

### 2. Test Script
```bash
python test_excel_file.py "file.xlsx"
```

**Output yang diharapkan:**
```
🧪 LAPORAN TESTING FILE EXCEL
======================================================================

📁 INFORMASI FILE:
  - File ada: ✅
  - Ukuran file: 15,234 bytes
  - Ekstensi: .xlsx

🧪 HASIL TESTING:
  - Total test: 9
  - Berhasil: 8
  - Gagal: 1

✅ TEST YANG BERHASIL:
  📋 Default:
    - Baris: 100
    - Kolom: 15
    - Parameter: {}

🏆 HASIL TERBAIK:
  - Test: Header 0 + NA Values
  - Baris: 100
  - Kolom: 15
  - Parameter: {'header': 0, 'na_values': ['', ' ', '-', 'N/A', 'NULL']}
```

## Kontak Support

Jika masalah masih berlanjut:
1. Jalankan script debugging dan testing
2. Simpan output sebagai file log
3. Kirim file Excel dan log ke tim development
4. Sertakan informasi sistem (OS, Python version, pandas version)

