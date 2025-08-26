# Data Analytics Visualization Web

Aplikasi web untuk analisis dan visualisasi data kesehatan dengan fokus pada analisis keuangan.

## Fitur Utama

### 1. Upload Data
- Upload file .txt dengan format tab-separated
- Mendukung data kesehatan dengan kolom yang lengkap
- Validasi format file otomatis

### 2. Analisis Keuangan
Sub menu keuangan menampilkan tabel dengan kolom-kolom berikut:

**Kolom Dasar:**
- KODE_RS
- KELAS_RS  
- KELAS_RAWAT
- KODE_TARIF
- ADMISSION_DATE
- DISCHARGE_DATE
- LOS (Length of Stay)
- NAMA_PASIEN
- NO_KARTU
- TOTAL_TARIF
- TARIF_RS

**Kolom Perhitungan:**
- TOTAL_TARIF/HARI = TOTAL_TARIF ÷ LOS
- TARIF_RS/HARI = TARIF_RS ÷ LOS
- LABA = TOTAL_TARIF - TARIF_RS (jika positif, jika negatif = 0)
- LABA/HARI = LABA ÷ LOS
- RUGI = |TOTAL_TARIF - TARIF_RS| (jika negatif, jika positif = 0)
- RUGI/HARI = RUGI ÷ LOS

## Cara Penggunaan

1. **Jalankan Aplikasi:**
   ```bash
   python app.py
   ```

2. **Buka Browser:**
   - Akses `http://localhost:5000`

3. **Upload Data:**
   - Klik "Upload .txt File" di sidebar
   - Pilih file .txt dengan format yang sesuai
   - Klik "Process File"

4. **Lihat Analisis Keuangan:**
   - Klik menu "Analytics" → "Keuangan"
   - Tabel akan menampilkan data dengan perhitungan keuangan

## Format Data

File .txt harus memiliki header dengan kolom-kolom berikut:
```
KODE_RS	KELAS_RS	KELAS_RAWAT	KODE_TARIF	ADMISSION_DATE	DISCHARGE_DATE	LOS	NAMA_PASIEN	NOKARTU	TOTAL_TARIF	TARIF_RS
```

## Dependencies

- Flask
- Pandas
- NumPy
- Matplotlib
- Plotly
- OpenPyXL

## Instalasi

1. Clone repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python app.py
   ```

## Struktur Proyek

```
DataAnalytics-VisualizationWeb/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sampel_data.txt       # Sample data file
├── processing/
│   ├── __init__.py       # Package initialization
│   └── data_handler.py   # Data processing logic
├── static/
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript functionality
├── templates/
│   └── index.html        # Main HTML template
└── instance/
    └── uploads/          # Temporary upload directory
```

## Catatan

- Semua perhitungan keuangan dilakukan secara otomatis
- Data yang diupload akan diproses dan ditampilkan dalam format tabel yang rapi
- Kolom laba/rugi di-highlight dengan warna berbeda untuk memudahkan analisis
- Aplikasi mendukung scroll horizontal untuk tabel dengan banyak kolom

## Arsitektur Kode

Aplikasi menggunakan arsitektur modular dengan pemisahan yang jelas:

### `app.py`
- File utama Flask application
- Menangani routing dan request/response
- Menggunakan DataHandler untuk pemrosesan data

### `processing/data_handler.py`
- Class `DataHandler` yang menangani semua logika pemrosesan data
- Fungsi untuk upload, validasi, dan perhitungan keuangan
- Pemisahan yang jelas antara logika bisnis dan presentation layer

### Keuntungan Refactoring
- **Maintainability**: Kode lebih mudah dipelihara dan diupdate
- **Testability**: Logika bisnis dapat di-test secara terpisah
- **Reusability**: DataHandler dapat digunakan di bagian lain aplikasi
- **Separation of Concerns**: Pemisahan yang jelas antara web layer dan business logic
