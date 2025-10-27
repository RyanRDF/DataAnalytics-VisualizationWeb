# INACBG Pricing Adjustments - Dokumentasi Sederhana

## 🎯 Apa Itu Fitur Ini?
Sistem otomatis menyesuaikan harga berdasarkan digit ke-4 dari kode INACBG saat upload data.

## 📋 Aturan Penyesuaian Harga

| Digit ke-4 INACBG | Penyesuaian | Contoh |
|-------------------|-------------|---------|
| **0** | 79% dari nilai asli | INACBG "1230" → semua harga × 0.79 |
| **I, II, III** | 73% dari nilai asli | INACBG "123I" → semua harga × 0.73 |
| **Lainnya** | 100% (tidak ada penyesuaian) | INACBG "1234" → harga tetap |

## 🔧 Kolom yang Disesuaikan
- `TOTAL_TARIF`
- `TARIF_RS` 
- `SELISIH`
- `PENUNJANG`
- `RADIOLOGI`
- `LABORATORIUM`

## 🚀 Cara Kerja
1. **Upload file** seperti biasa
2. **Sistem otomatis** cek digit ke-4 INACBG
3. **Harga disesuaikan** sesuai aturan
4. **Data disimpan** ke database dengan harga yang sudah disesuaikan

## 📊 Contoh Hasil
```
Data diproses: 100 baris berhasil
Penyesuaian harga: 
- 50 baris (digit 4='0', 79%)
- 30 baris (digit 4='I/II/III', 73%) 
- 20 baris (tanpa penyesuaian)
```

## ⚠️ Catatan Penting
- ✅ Hanya berlaku untuk data baru yang diupload
- ✅ Data lama di database tidak berubah
- ✅ Proses otomatis, tidak perlu setting manual
- ✅ Semua penyesuaian dicatat dalam log

## 🔍 Troubleshooting
**Penyesuaian tidak berlaku?**
- Pastikan INACBG minimal 4 digit
- Pastikan kolom harga berisi angka
- Cek log untuk error messages

**Nilai tidak sesuai?**
- Pastikan digit ke-4 tepat: '0', 'I', 'II', atau 'III'
- Case sensitive untuk 'I', 'II', 'III'
