# Fitur Filter Data Pasien Dashboard

## Overview
Submenu Pasien telah diperluas dengan 3 fitur filter yang sama seperti submenu Keuangan, namun disesuaikan untuk data pasien dengan kolom-kolom yang relevan.

## Fitur Filter yang Tersedia

### 1. Sorting Controls (Filter Pengurutan)
- **Lokasi**: Di atas tabel data pasien
- **Fungsi**: Mengurutkan data pasien berdasarkan kolom tertentu
- **Komponen**:
  - Dropdown untuk memilih kolom pengurutan
  - Dropdown untuk memilih urutan (ASC/DESC)
  - Tombol "Apply Sort" untuk menerapkan pengurutan

### 2. Date Range Filter Controls (Filter Berdasarkan Rentang Waktu)
- **Lokasi**: Di bawah sorting controls
- **Fungsi**: Memfilter data pasien berdasarkan rentang tanggal admission
- **Komponen**:
  - Input tanggal untuk tanggal mulai
  - Input tanggal untuk tanggal akhir
  - Tombol "Filter Data" untuk menerapkan filter
  - Tombol "Clear Filter" untuk membersihkan filter

### 3. Specific Data Filter Controls (Filter Data Spesifik)
- **Lokasi**: Di bawah date range filter controls
- **Fungsi**: Memfilter data pasien berdasarkan nilai spesifik pada kolom tertentu
- **Komponen**:
  - Dropdown untuk memilih kolom yang akan difilter
  - Input text untuk memasukkan nilai yang dicari
  - Tombol "Cari" untuk menerapkan filter
  - Tombol "Clear" untuk membersihkan filter

## Kolom-kolom yang Tersedia untuk Filter

### Kolom Numerik (Sorting & Filtering)
- **LOS**: Length of Stay (durasi rawat inap)
- **BIRTH_WEIGHT**: Berat badan lahir
- **UMUR_TAHUN**: Umur dalam tahun
- **UMUR_HARI**: Umur dalam hari

### Kolom String (Sorting & Filtering)
- **KODE_RS**: Kode rumah sakit
- **KELAS_RS**: Kelas rumah sakit
- **KELAS_RAWAT**: Kelas rawat
- **KODE_TARIF**: Kode tarif
- **NAMA_PASIEN**: Nama pasien
- **NOKARTU**: Nomor kartu
- **SEX**: Jenis kelamin
- **DISCHARGE_STATUS**: Status discharge
- **DIAGLIST**: Daftar diagnosis
- **PROCLIST**: Daftar prosedur
- **DPJP**: Dokter penanggung jawab
- **SEP**: Surat Eligibilitas Pasien
- **PAYOR_ID**: ID pembayar
- **CODER_ID**: ID coder
- **VERSI_INACBG**: Versi INACBG
- **VERSI_GROUPER**: Versi grouper

### Kolom Tanggal (Date Filtering)
- **ADMISSION_DATE**: Tanggal masuk
- **DISCHARGE_DATE**: Tanggal keluar
- **BIRTH_DATE**: Tanggal lahir

## Cara Penggunaan

### Filter Data Spesifik
1. **Pilih Kolom**: Gunakan dropdown untuk memilih kolom yang ingin difilter
2. **Masukkan Nilai**: Ketik nilai yang ingin dicari dalam kolom tersebut
3. **Terapkan Filter**: Klik tombol "Cari" untuk menerapkan filter
4. **Bersihkan Filter**: Klik tombol "Clear" untuk membersihkan filter

### Kombinasi Filter
Semua filter dapat digunakan secara bersamaan:
- Sorting + Date Range + Specific Filter
- Sorting + Specific Filter
- Date Range + Specific Filter
- Hanya Specific Filter saja

## Fitur Teknis

### Backend Endpoints
- `/pasien/sort` - Endpoint untuk sorting data pasien
- `/pasien/filter` - Endpoint untuk date filtering data pasien
- `/pasien/specific-filter` - Endpoint untuk specific filtering data pasien
- `/pasien/columns` - Endpoint untuk mendapatkan daftar kolom yang tersedia

### Frontend Features
- **Real-time Filtering**: Filter diterapkan secara real-time
- **Loading States**: Tombol menunjukkan status loading saat memproses
- **Error Handling**: Pesan error yang informatif
- **Responsive Design**: Interface yang responsif untuk berbagai ukuran layar

### Algoritma Filtering
- **Case-insensitive Search**: Pencarian tidak membedakan huruf besar/kecil
- **Smart Column Detection**: Otomatis mendeteksi tipe data kolom
- **Flexible Matching**: Mendukung exact match untuk numerik dan partial match untuk string
- **Date Handling**: Mendukung format DD/MM/YYYY dari data asli

## Styling dan UI

### Color Scheme
- **Sorting Controls**: Biru (#f8f9fa)
- **Date Filter Controls**: Hijau (#e8f5e8)
- **Specific Filter Controls**: Kuning (#fff3cd)

### Responsive Layout
- Flexbox layout untuk alignment yang baik
- Gap spacing yang konsisten
- Hover effects pada tombol
- Focus states pada input fields

## Contoh Penggunaan

### Skenario 1: Mencari Pasien Tertentu
1. Pilih kolom "NAMA_PASIEN"
2. Masukkan nama pasien (misal: "John")
3. Klik "Cari"
4. Data akan difilter untuk menampilkan pasien dengan nama yang mengandung "John"

### Skenario 2: Mencari Data dengan Nilai Numerik Tertentu
1. Pilih kolom "LOS"
2. Masukkan nilai (misal: "5")
3. Klik "Cari"
4. Data akan difilter untuk menampilkan pasien dengan LOS 5 hari

### Skenario 3: Kombinasi Filter
1. Set sorting berdasarkan "UMUR_TAHUN" DESC
2. Set date range untuk bulan tertentu
3. Set specific filter untuk kolom "SEX" dengan nilai "L"
4. Hasil akan menampilkan data pasien laki-laki yang memenuhi semua kriteria

### Skenario 4: Filter Berdasarkan Diagnosis
1. Pilih kolom "DIAGLIST"
2. Masukkan diagnosis (misal: "diabetes")
3. Klik "Cari"
4. Data akan difilter untuk menampilkan pasien dengan diagnosis yang mengandung "diabetes"

## Troubleshooting

### Filter Tidak Berfungsi
- Pastikan file data sudah diupload
- Periksa apakah kolom yang dipilih tersedia dalam data
- Pastikan nilai yang dimasukkan sesuai dengan tipe data kolom

### Data Tidak Ditemukan
- Coba gunakan nilai yang lebih umum
- Periksa apakah ada spasi atau karakter khusus
- Gunakan partial search (tidak perlu exact match)

### Error pada Date Filter
- Pastikan format tanggal yang dimasukkan valid (YYYY-MM-DD)
- Periksa apakah kolom ADMISSION_DATE tersedia dalam data
- Pastikan data tanggal dalam format DD/MM/YYYY

## Perbedaan dengan Fitur Keuangan

### Kolom yang Berbeda
- **Keuangan**: Fokus pada kolom finansial (TOTAL_TARIF, TARIF_RS, LABA, RUGI)
- **Pasien**: Fokus pada kolom medis (NAMA_PASIEN, DIAGLIST, PROCLIST, DPJP)

### Perhitungan yang Berbeda
- **Keuangan**: Memiliki perhitungan derivatif (LABA/HARI, RUGI/HARI)
- **Pasien**: Fokus pada data demografis dan medis

### Endpoint yang Berbeda
- **Keuangan**: `/keuangan/*`
- **Pasien**: `/pasien/*`

## Future Enhancements
- **Advanced Medical Search**: Filter berdasarkan kombinasi diagnosis dan prosedur
- **Age Group Filtering**: Filter berdasarkan kelompok umur
- **Medical History Filtering**: Filter berdasarkan riwayat medis
- **Export Filtered Patient Data**: Export hasil filter ke file
- **Patient Statistics**: Statistik berdasarkan hasil filter
