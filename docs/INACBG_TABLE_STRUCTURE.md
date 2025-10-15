# 📊 Struktur Tabel Analisis INACBG

## Overview
Tabel Analisis INACBG menampilkan data yang sudah dikelompokkan berdasarkan kode INACBG dengan statistik agregat untuk setiap kelompok.

## 🔍 Cara Kerja
1. **Data di-group** berdasarkan `INACBG` dan `DESKRIPSI_INACBG`
2. **Statistik dihitung** untuk setiap kelompok:
   - Jumlah pasien
   - Rata-rata, minimum, dan maksimum LOS
   - Rata-rata dan total tarif
3. **Data diformat** dengan format Rupiah untuk kolom mata uang

## 📋 Struktur Kolom Tabel

### Kolom Identitas
| Kolom | Deskripsi | Contoh |
|-------|-----------|---------|
| `INACBG` | Kode INACBG | `K-4-17-I` |
| `DESKRIPSI_INACBG` | Deskripsi INACBG | `NYERI ABDOMEN & GASTROENTERITIS LAIN-LAIN (RINGAN)` |

### Kolom Statistik Pasien
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `jumlah_pasien` | Jumlah pasien dalam kelompok | Angka |

### Kolom LOS (Length of Stay)
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `rata_rata_los` | Rata-rata lama rawat inap | Angka (hari) |
| `min_los` | Lama rawat inap terpendek | Angka (hari) |
| `max_los` | Lama rawat inap terpanjang | Angka (hari) |

### Kolom Tarif (Formatted)
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `rata_rata_total_tarif_formatted` | Rata-rata total tarif | `Rp. 2.430.100` |
| `total_tarif_formatted` | Total tarif semua pasien | `Rp. 4.860.200` |
| `rata_rata_tarif_rs_formatted` | Rata-rata tarif RS | `Rp. 7.911.914` |
| `total_tarif_rs_formatted` | Total tarif RS semua pasien | `Rp. 15.823.828` |
| `selisih_tarif_formatted` | Selisih rata-rata tarif | `Rp. -5.481.814` |

### Kolom Persentase
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `persentase_selisih` | Persentase selisih tarif | Angka (%), contoh: `-69.3` |

## 🎯 Contoh Data

```
INACBG: K-4-17-I
DESKRIPSI_INACBG: NYERI ABDOMEN & GASTROENTERITIS LAIN-LAIN (RINGAN)
jumlah_pasien: 2
rata_rata_los: 4.0
min_los: 3
max_los: 5
rata_rata_total_tarif_formatted: Rp. 2.430.100
total_tarif_formatted: Rp. 4.860.200
rata_rata_tarif_rs_formatted: Rp. 7.911.914
total_tarif_rs_formatted: Rp. 15.823.828
selisih_tarif_formatted: Rp. -5.481.814
persentase_selisih: -69.3
```

## 🔧 Fitur Tabel

### Sorting
- Bisa diurutkan berdasarkan kolom apapun
- ASC (Ascending) atau DESC (Descending)

### Filtering
- Filter berdasarkan kolom tertentu
- Pencarian nilai spesifik

### Format Mata Uang
- Semua nilai mata uang ditampilkan dalam format Rupiah
- Format: `Rp. 1.000.000` (dengan pemisah ribuan)

## 📈 Manfaat Analisis

1. **Identifikasi Kelompok INACBG** yang paling banyak pasiennya
2. **Analisis LOS** untuk setiap kelompok penyakit
3. **Perbandingan Tarif** antara tarif yang dikenakan vs tarif standar
4. **Identifikasi Selisih** yang signifikan untuk evaluasi lebih lanjut
5. **Statistik Agregat** untuk laporan manajemen

## 🚀 Cara Menggunakan

1. Pilih menu "Analisis INACBG"
2. Tentukan rentang tanggal
3. Klik "SEARCH" untuk menampilkan data
4. Gunakan dropdown "Sort By" untuk mengurutkan data
5. Gunakan filter untuk mencari data spesifik

