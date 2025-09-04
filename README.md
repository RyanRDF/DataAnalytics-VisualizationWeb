# 📊 Data Analytics Dashboard

Aplikasi web untuk analisis data medis dengan fitur pemrosesan otomatis berdasarkan INACBG dan sistem penyimpanan dataset yang cerdas.

## 🚀 Fitur Utama

### 📁 **Upload & Pemrosesan Data**
- Upload file `.txt` dengan format tab-separated
- **Pemrosesan Otomatis**: Data diproses berdasarkan digit ke-4 INACBG
  - Digit '0' → Harga dikalikan 79%
  - Digit 'I/II/III' → Harga dikalikan 73%
- **Penyimpanan Dataset**: Data tersimpan otomatis untuk akses cepat

### 🔄 **Dataset Switcher**
- Dropdown di pojok kanan atas untuk beralih antar dataset
- Menampilkan nama file dan waktu upload
- Beralih dataset tanpa perlu upload ulang

### 📈 **Menu Analisis**

#### **E-Claim**
- **Keuangan**: Analisis laba rugi dengan perhitungan otomatis
- **Pasien**: Informasi medis lengkap pasien

#### **Analisa**
- **Selisih Tarif**: Perbandingan tarif claim vs billing RS
- **LOS**: Analisis lama rawat inap pasien
- **INACBG**: Pengelompokan data berdasarkan INACBG
- **Ventilator**: Analisis penggunaan ventilator

### 🔍 **Fitur Filter & Sort**
- **Filter Tanggal**: Rentang waktu admission
- **Sorting**: Berdasarkan kolom apapun (ASC/DESC)
- **Filter Spesifik**: Pencarian berdasarkan nilai kolom
- **Clear Filter**: Reset semua filter

## 🛠️ Cara Instalasi

### 1. **Persyaratan Sistem**
- Python 3.7+
- Browser modern (Chrome, Firefox, Safari, Edge)

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Jalankan Aplikasi**
```bash
python app.py
```

### 4. **Akses Aplikasi**
Buka browser dan kunjungi: `http://localhost:5000`

## 📖 Cara Penggunaan

### **Langkah 1: Upload Data**
1. Klik "Choose File" di sidebar
2. Pilih file `.txt` yang ingin dianalisis
3. Klik "Process File"
4. Data akan diproses dan tersimpan otomatis

### **Langkah 2: Pilih Analisis**
1. Klik menu yang diinginkan di sidebar:
   - **E-Claim** → Keuangan atau Pasien
   - **Analisa** → Selisih Tarif, LOS, INACBG, atau Ventilator

### **Langkah 3: Filter Data**
1. **Filter Tanggal** (opsional):
   - Pilih tanggal mulai dan akhir
   - Klik "Filter Data"

2. **Sorting** (opsional):
   - Pilih kolom untuk sorting
   - Pilih urutan (ASC/DESC)
   - Klik "Apply Sort"

3. **Filter Spesifik** (opsional):
   - Pilih kolom yang ingin difilter
   - Masukkan nilai yang dicari
   - Klik "Cari"

### **Langkah 4: Beralih Dataset**
1. Klik dropdown di pojok kanan atas
2. Pilih dataset yang ingin digunakan
3. Data akan berubah secara otomatis

## 📊 Format Data Input

File harus berformat **tab-separated (.txt)** dengan kolom:
- `INACBG` - Kode INACBG (format: K-4-17-I)
- `TARIF_RS` - Tarif rumah sakit
- `PENUNJANG` - Biaya penunjang
- `RADIOLOGI` - Biaya radiologi
- `LABORATORIUM` - Biaya laboratorium
- `ADMISSION_DATE` - Tanggal masuk (DD/MM/YYYY)
- `DISCHARGE_DATE` - Tanggal keluar (DD/MM/YYYY)
- `LOS` - Lama rawat inap
- `NAMA_PASIEN` - Nama pasien
- Dan kolom lainnya sesuai kebutuhan

## 🔧 Struktur Aplikasi

```
DataAnalytics-VisualizationWeb/
├── app.py                 # Aplikasi Flask utama
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html        # Template HTML
├── static/
│   ├── style.css         # Styling CSS
│   └── script.js         # JavaScript
├── processing/
│   ├── data_handler.py   # Handler utama
│   ├── data_processor.py # Pemrosesan INACBG
│   ├── data_storage.py   # Penyimpanan dataset
│   └── *_handler.py      # Handler khusus per menu
└── saved_data/           # Dataset tersimpan
    ├── metadata.json     # Metadata dataset
    └── *.pkl            # File data
```

## ⚡ Keunggulan

- **Pemrosesan Otomatis**: Data diproses sesuai aturan INACBG
- **Dataset Management**: Simpan dan beralih antar dataset dengan mudah
- **Interface Modern**: UI yang responsif dan user-friendly
- **Filter Canggih**: Multiple filter dan sorting options
- **Real-time Updates**: Perubahan data langsung terlihat
- **Mobile Friendly**: Bekerja di desktop dan mobile

## 🐛 Troubleshooting

### **Error "No data available"**
- Pastikan file sudah diupload
- Periksa format file (harus .txt dengan tab separator)

### **Error "Missing columns"**
- Pastikan file memiliki kolom yang diperlukan
- Periksa nama kolom sesuai format yang diminta

### **Dataset tidak muncul**
- Klik tombol "🔄 Refresh" di dropdown dataset
- Pastikan file sudah berhasil diupload

## 📝 Dependencies

- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

## 🤝 Kontribusi

Silakan buat issue atau pull request untuk perbaikan dan fitur baru.

## 📄 Lisensi

Proyek ini dibuat untuk keperluan analisis data medis.