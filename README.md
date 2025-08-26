# Data Analytics Visualization Web

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplikasi web untuk analisis dan visualisasi data kesehatan dengan fokus pada analisis keuangan dan data pasien. Dibangun dengan Flask dan Pandas untuk pemrosesan data yang efisien.

## 🚀 Fitur Utama

### 📊 Analisis Keuangan
- **Perhitungan Otomatis**: Laba rugi berdasarkan tarif rumah sakit
- **Kolom Perhitungan**: 
  - TOTAL_TARIF/HARI = TOTAL_TARIF ÷ LOS
  - TARIF_RS/HARI = TARIF_RS ÷ LOS
  - LABA = TOTAL_TARIF - TARIF_RS (jika positif)
  - LABA/HARI = LABA ÷ LOS
  - RUGI = |TOTAL_TARIF - TARIF_RS| (jika negatif)
  - RUGI/HARI = RUGI ÷ LOS

### 👥 Data Pasien
- **Informasi Lengkap**: Data pasien dengan 38 kolom informasi medis
- **Highlight Kolom Penting**: KODE_RS, NAMA_PASIEN, NOKARTU, MRN
- **Data Cleaning**: Otomatis membersihkan data yang tidak lengkap

### 📁 Upload Data
- **Format Fleksibel**: Mendukung file .txt dengan tab-separated
- **Validasi Otomatis**: Pengecekan format file dan struktur data
- **Error Handling**: Pesan error yang informatif

## 📋 Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda memiliki:

- **Python 3.8 atau lebih baru**
- **pip** (package installer untuk Python)
- **Git** (untuk clone repository)

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/username/DataAnalytics-VisualizationWeb.git
cd DataAnalytics-VisualizationWeb
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Cara Menjalankan

### 1. Jalankan Aplikasi
```bash
python app.py
```

### 2. Buka Browser
Akses aplikasi di: `http://localhost:5000`

### 3. Upload Data
1. Klik "Upload .txt File" di sidebar
2. Pilih file .txt dengan format yang sesuai
3. Klik "Process File"

### 4. Lihat Analisis
- **Keuangan**: Klik menu "Analytics" → "Keuangan"
- **Pasien**: Klik menu "Analytics" → "Pasien"

## 📁 Format Data

File .txt harus memiliki header dengan kolom-kolom berikut:

```
KODE_RS	KELAS_RS	KELAS_RAWAT	KODE_TARIF	ADMISSION_DATE	DISCHARGE_DATE	LOS	NAMA_PASIEN	NOKARTU	TOTAL_TARIF	TARIF_RS
```

### Contoh Data
```
KODE_RS	KELAS_RS	KELAS_RAWAT	KODE_TARIF	ADMISSION_DATE	DISCHARGE_DATE	LOS	NAMA_PASIEN	NOKARTU	TOTAL_TARIF	TARIF_RS
36720XX	B	1	BS	27/06/2025	01/07/2025	5	AN. AZ	0003567212345	2430100	7911914
36720XX	B	3	BS	28/06/2025	01/07/2025	4	NY.S	0001230212345	4466500	6121404
```

## 📦 Dependencies

| Package | Version | Description |
|---------|---------|-------------|
| Flask | 2.0+ | Web framework |
| Pandas | 1.3+ | Data manipulation |
| NumPy | 1.21+ | Numerical computing |
| Matplotlib | 3.4+ | Plotting library |
| Plotly | 5.0+ | Interactive charts |
| OpenPyXL | 3.0+ | Excel file support |

## 🏗️ Struktur Proyek

```
DataAnalytics-VisualizationWeb/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sampel_data.txt       # Sample data file
├── README.md             # Project documentation
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

## 🔧 Konfigurasi

### Environment Variables (Opsional)
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Production
export FLASK_ENV=production
```

### Port Configuration
Untuk mengubah port default (5000), edit `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Ganti port di sini
```

## 🧪 Testing

### Manual Testing
1. Upload file `sampel_data.txt` yang disediakan
2. Test fitur keuangan dan pasien
3. Verifikasi perhitungan laba rugi

### Unit Testing (Coming Soon)
```bash
python -m pytest tests/
```

## 🐛 Troubleshooting

### Error: "No module named 'pandas'"
```bash
pip install pandas
```

### Error: "Port already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Error: "File upload failed"
- Pastikan file berformat .txt
- Pastikan data tab-separated
- Periksa permission folder uploads

## 🤝 Contributing

1. Fork repository
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

- **Author**: [Nama Anda]
- **Email**: [email@example.com]
- **GitHub**: [@username](https://github.com/username)

## 🙏 Acknowledgments

- Flask community untuk framework yang luar biasa
- Pandas team untuk library data manipulation
- Bootstrap untuk styling components

## 📈 Roadmap

- [ ] Tambah fitur export ke Excel
- [ ] Implementasi grafik interaktif
- [ ] Dashboard real-time
- [ ] API endpoints
- [ ] Database integration
- [ ] User authentication

---

⭐ Jika project ini membantu Anda, jangan lupa berikan star!
