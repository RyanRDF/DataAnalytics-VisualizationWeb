# 🫁 Struktur Tabel Analisis Ventilator

## Overview
Tabel Analisis Ventilator menampilkan data pasien dengan informasi penggunaan ventilator, termasuk pasien yang menggunakan dan tidak menggunakan ventilator.

## 🔍 Cara Kerja
1. **Data diambil** dari semua pasien (termasuk yang tidak menggunakan ventilator)
2. **Metrik ventilator dihitung** untuk setiap pasien:
   - Hari penggunaan ventilator
   - Biaya per jam ventilator
   - Biaya per hari ventilator
   - Persentase penggunaan ventilator dari total LOS
3. **Status ventilator** ditampilkan untuk setiap pasien
4. **Data diformat** dengan format Rupiah untuk kolom mata uang

## 📋 Struktur Kolom Tabel

### Kolom Identitas Pasien
| Kolom | Deskripsi | Contoh |
|-------|-----------|---------|
| `SEP` | Nomor Surat Eligibilitas Peserta | `0224R0020625V014657` |
| `MRN` | Medical Record Number | `0139-25-87` |
| `NAMA_PASIEN` | Nama Pasien | `AN. AZ` |
| `INACBG` | Kode INACBG | `K-4-17-I` |
| `DESKRIPSI_INACBG` | Deskripsi INACBG | `NYERI ABDOMEN & GASTROENTERITIS LAIN-LAIN (RINGAN)` |

### Kolom Rawat Inap
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `LOS` | Length of Stay (hari) | Angka |
| `ADMISSION_DATE` | Tanggal Masuk | Date |
| `DISCHARGE_DATE` | Tanggal Keluar | Date |

### Kolom Ventilator
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `VENT_HOUR` | Jam penggunaan ventilator | Angka (jam) |
| `VENTILATOR_DAYS` | Hari penggunaan ventilator | Angka (hari) |
| `VENTILATOR_STATUS` | Status penggunaan ventilator | `Menggunakan Ventilator` / `Tidak Menggunakan Ventilator` |
| `VENTILATOR_PERCENTAGE_OF_TOTAL` | Persentase ventilator dari total LOS | Angka (%) |

### Kolom ICU
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `ICU_INDIKATOR` | Indikator ICU | Angka (0/1) |
| `ICU_LOS` | Lama rawat di ICU | Angka (hari) |

### Kolom Tarif (Formatted)
| Kolom | Deskripsi | Format |
|-------|-----------|---------|
| `TOTAL_TARIF_FORMATTED` | Total tarif pasien | `Rp. 2.430.100` |
| `TARIF_RS_FORMATTED` | Tarif rumah sakit | `Rp. 7.911.914` |
| `VENTILATOR_COST_PER_HOUR_FORMATTED` | Biaya ventilator per jam | `Rp. 0` (jika tidak menggunakan) |
| `VENTILATOR_COST_PER_DAY_FORMATTED` | Biaya ventilator per hari | `Rp. 0` (jika tidak menggunakan) |

## 🎯 Contoh Data

### Pasien yang Menggunakan Ventilator
```
SEP: 0224R0020625V014657
MRN: 0139-25-87
NAMA_PASIEN: AN. AZ
INACBG: K-4-17-I
LOS: 5
VENT_HOUR: 24
VENTILATOR_DAYS: 1.0
VENTILATOR_STATUS: Menggunakan Ventilator
VENTILATOR_PERCENTAGE_OF_TOTAL: 20.0
TOTAL_TARIF_FORMATTED: Rp. 2.430.100
VENTILATOR_COST_PER_HOUR_FORMATTED: Rp. 101.254
VENTILATOR_COST_PER_DAY_FORMATTED: Rp. 2.430.100
```

### Pasien yang Tidak Menggunakan Ventilator
```
SEP: 0224R0020625V014788
MRN: 0143-71-70
NAMA_PASIEN: NY. S
INACBG: B-4-14-I
LOS: 4
VENT_HOUR: 0
VENTILATOR_DAYS: 0.0
VENTILATOR_STATUS: Tidak Menggunakan Ventilator
VENTILATOR_PERCENTAGE_OF_TOTAL: 0.0
TOTAL_TARIF_FORMATTED: Rp. 4.466.500
VENTILATOR_COST_PER_HOUR_FORMATTED: Rp. 0
VENTILATOR_COST_PER_DAY_FORMATTED: Rp. 0
```

## 🔧 Fitur Tabel

### Sorting
- Bisa diurutkan berdasarkan kolom apapun
- ASC (Ascending) atau DESC (Descending)

### Filtering
- Filter berdasarkan kolom tertentu
- Pencarian nilai spesifik
- Filter berdasarkan status ventilator

### Format Mata Uang
- Semua nilai mata uang ditampilkan dalam format Rupiah
- Format: `Rp. 1.000.000` (dengan pemisah ribuan)

### Penanganan Data Kosong
- Biaya ventilator = 0 untuk pasien yang tidak menggunakan ventilator
- Persentase ventilator = 0% untuk pasien yang tidak menggunakan ventilator
- Status ventilator ditampilkan dengan jelas

## 📈 Manfaat Analisis

1. **Identifikasi Pasien** yang menggunakan ventilator
2. **Analisis Biaya Ventilator** per jam dan per hari
3. **Perbandingan Biaya** antara pasien dengan dan tanpa ventilator
4. **Analisis Efisiensi** penggunaan ventilator
5. **Statistik ICU** dan hubungannya dengan ventilator
6. **Laporan Manajemen** untuk perencanaan sumber daya ventilator

## 🚀 Cara Menggunakan

1. Pilih menu "Analisis Ventilator"
2. Tentukan rentang tanggal
3. Klik "SEARCH" untuk menampilkan data
4. Gunakan dropdown "Sort By" untuk mengurutkan data
5. Gunakan filter untuk mencari data spesifik
6. Perhatikan kolom `VENTILATOR_STATUS` untuk membedakan pasien

## ⚠️ Catatan Penting

- **Data Kosong**: Jika tidak ada data ventilator, tabel akan kosong
- **Biaya Nol**: Pasien yang tidak menggunakan ventilator akan memiliki biaya ventilator = 0
- **Persentase**: Persentase ventilator dihitung dari total LOS pasien
- **Status**: Kolom `VENTILATOR_STATUS` membantu membedakan pasien dengan mudah

