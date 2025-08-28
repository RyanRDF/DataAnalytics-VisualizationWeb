# Fitur Filter Data Analytics Dashboard

## Overview
Dashboard Data Analytics telah diperluas dengan fitur filter yang lebih canggih untuk memungkinkan pengguna melakukan pencarian dan filtering data yang lebih spesifik.

## Fitur Filter yang Tersedia

### 1. Sorting Controls (Filter Pengurutan)
- **Lokasi**: Di atas tabel data keuangan
- **Fungsi**: Mengurutkan data berdasarkan kolom tertentu
- **Komponen**:
  - Dropdown untuk memilih kolom pengurutan
  - Dropdown untuk memilih urutan (ASC/DESC)
  - Tombol "Apply Sort" untuk menerapkan pengurutan

### 2. Date Range Filter Controls (Filter Berdasarkan Rentang Waktu)
- **Lokasi**: Di bawah sorting controls
- **Fungsi**: Memfilter data berdasarkan rentang tanggal
- **Komponen**:
  - Input tanggal untuk tanggal mulai
  - Input tanggal untuk tanggal akhir
  - Tombol "Filter Data" untuk menerapkan filter
  - Tombol "Clear Filter" untuk membersihkan filter

### 3. Specific Data Filter Controls (Filter Data Spesifik) ⭐ **BARU**
- **Lokasi**: Di bawah date range filter controls
- **Fungsi**: Memfilter data berdasarkan nilai spesifik pada kolom tertentu
- **Komponen**:
  - Dropdown untuk memilih kolom yang akan difilter
  - Input text untuk memasukkan nilai yang dicari
  - Tombol "Cari" untuk menerapkan filter
  - Tombol "Clear" untuk membersihkan filter

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
- `/keuangan/specific-filter` - Endpoint baru untuk filter spesifik
- Mendukung kombinasi dengan sorting dan date filtering

### Frontend Features
- **Real-time Filtering**: Filter diterapkan secara real-time
- **Loading States**: Tombol menunjukkan status loading saat memproses
- **Error Handling**: Pesan error yang informatif
- **Responsive Design**: Interface yang responsif untuk berbagai ukuran layar

### Algoritma Filtering
- **Case-insensitive Search**: Pencarian tidak membedakan huruf besar/kecil
- **Smart Column Detection**: Otomatis mendeteksi tipe data kolom
- **Flexible Matching**: Mendukung exact match untuk numerik dan partial match untuk string

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
1. Pilih kolom "TOTAL_TARIF"
2. Masukkan nilai (misal: "1000000")
3. Klik "Cari"
4. Data akan difilter untuk menampilkan transaksi dengan total tarif 1 juta

### Skenario 3: Kombinasi Filter
1. Set sorting berdasarkan "LABA" DESC
2. Set date range untuk bulan tertentu
3. Set specific filter untuk kolom "TARIF_RS" dengan nilai "500000"
4. Hasil akan menampilkan data yang memenuhi semua kriteria

## Troubleshooting

### Filter Tidak Berfungsi
- Pastikan file data sudah diupload
- Periksa apakah kolom yang dipilih tersedia dalam data
- Pastikan nilai yang dimasukkan sesuai dengan tipe data kolom

### Data Tidak Ditemukan
- Coba gunakan nilai yang lebih umum
- Periksa apakah ada spasi atau karakter khusus
- Gunakan partial search (tidak perlu exact match)

## Future Enhancements
- **Advanced Search**: Regex pattern matching
- **Multiple Column Filter**: Filter berdasarkan beberapa kolom sekaligus
- **Saved Filters**: Menyimpan filter yang sering digunakan
- **Export Filtered Data**: Export hasil filter ke file
- **Filter History**: Riwayat filter yang telah digunakan
