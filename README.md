# Data Analytics Visualization Web

Aplikasi web untuk analisis dan visualisasi data dengan fitur filtering, sorting, dan analisis berbagai jenis data.

## Fitur Utama

- **Upload File**: Upload file .txt dengan format tab-separated
- **Menu E-Claim**: 
  - Analisis Keuangan (dengan perhitungan laba rugi)
  - Analisis Pasien (informasi medis lengkap)
- **Menu Analisa**:
  - Analisa Selisih Tarif (selisih antara tarif yang dikenakan dan tarif standar)
  - Analisa LOS (Length of Stay - lama rawat inap pasien)

## Struktur Kode

### Frontend
- `templates/index.html` - Template HTML utama dengan sidebar dan konten
- `static/style.css` - Styling CSS
- `static/script.js` - JavaScript untuk interaksi dan state management

### Backend
- `app.py` - Flask application dengan routing untuk semua menu
- `processing/` - Modul untuk pemrosesan data
  - `__init__.py` - Import semua handler
  - `data_handler.py` - Handler utama yang mengkoordinasikan semua handler khusus
  - `financial_handler.py` - Handler khusus untuk data keuangan
  - `patient_handler.py` - Handler khusus untuk data pasien
  - `selisih_tarif_handler.py` - Handler khusus untuk analisa selisih tarif

## Struktur Data

### Analisis Keuangan
Kolom yang ditampilkan:
- KODE_RS, KELAS_RS, KELAS_RAWAT, KODE_TARIF
- ADMISSION_DATE, DISCHARGE_DATE, LOS, NAMA_PASIEN, NOKARTU
- TOTAL_TARIF, TARIF_RS
- TOTAL_TARIF/HARI, TARIF_RS/HARI, LABA, LABA/HARI, RUGI, RUGI/HARI

### Analisis Pasien
Kolom yang ditampilkan:
- KODE_RS, KELAS_RS, KELAS_RAWAT, KODE_TARIF
- ADMISSION_DATE, DISCHARGE_DATE, LOS, NAMA_PASIEN
- NOKARTU, BIRTH_DATE, BIRTH_WEIGHT, SEX, DISCHARGE_STATUS
- DIAGLIST, PROCLIST, ADL1, ADL2
- IN_SP, IN_SR, IN_SI, IN_SD, INACBG, SUBACUTE, CHRONIC
- SP, SR, SI, SD, DESKRIPSI_INACBG
- MRN, UMUR_TAHUN, UMUR_HARI, DPJP, SEP, PAYOR_ID
- CODER_ID, VERSI_INACBG, VERSI_GROUPER

### Analisa Selisih Tarif
Kolom yang ditampilkan:
- SEP, RM, LOS, PDX, SDX, PROCLIST, INACBG
- DESKRIPSI_INACBG, TOTAL_CLAIM, TOTAL_BILING_RS, SELISIH
- ADMISSION_DATE, DISCHARGE_DATE

**Keterangan kolom:**
- **SEP** = dari kolom SEP
- **RM** = dari kolom MRN
- **LOS** = dari kolom LOS
- **PDX** = Primary Diagnosis (index pertama dari DIAGLIST, sebelum separator `;`)
- **SDX** = Secondary Diagnosis (setelah separator `;` dari DIAGLIST)
- **PR** = dari PROCLIST
- **INACBG** = dari INACBG
- **DESC INACBG** = dari DESKRIPSI_INACBG
- **TOTAL_CLAIM** = dari TOTAL_TARIF
- **TOTAL_BILING RS** = dari TARIF_RS
- **SELISIH** = TOTAL_CLAIM - TOTAL_BILING_RS
- **ADMISSION_DATE** = dari ADMISSION_DATE
- **DISCHARGE_DATE** = dari DISCHARGE_DATE

### Analisa LOS (Length of Stay)
Kolom yang ditampilkan:
- SEP, MRN, PDX, SDX, PROCLIST, INACBG, LOS, CARA_PULANG
- TOTAL_CLAIM, TOTAL_BILING_RS, SELISIH
- ADMISSION_DATE, DISCHARGE_DATE

**Keterangan kolom:**
- **SEP** = dari kolom SEP
- **MRN** = dari kolom MRN
- **PDX** = Primary Diagnosis (index pertama dari DIAGLIST, sebelum separator `;`)
- **SDX** = Secondary Diagnosis (setelah separator `;` dari DIAGLIST)
- **PR** = dari PROCLIST
- **INACBG** = dari INACBG
- **LOS** = dari kolom LOS
- **CARA_PULANG** = dari DISCHARGE_STATUS (1=Persetujuan Dokter, 2=Dirujuk, 3=Persetujuan Sendiri, 4=Meninggal)
- **TOTAL_CLAIM** = dari TOTAL_TARIF
- **TOTAL_BILING RS** = dari TARIF_RS
- **SELISIH** = TOTAL_CLAIM - TOTAL_BILING_RS
- **ADMISSION_DATE** = dari ADMISSION_DATE
- **DISCHARGE_DATE** = dari DISCHARGE_DATE

## Fitur Filtering dan Sorting

Setiap menu memiliki fitur:
1. **Filter Tanggal**: Filter berdasarkan rentang tanggal admission
2. **Sorting**: Sort berdasarkan kolom tertentu (ASC/DESC)
3. **Filter Spesifik**: Filter berdasarkan nilai kolom tertentu
4. **Clear Filter**: Hapus semua filter yang diterapkan

## Cara Penggunaan

1. **Upload File**: Upload file .txt melalui form di sidebar
2. **Pilih Menu**: Klik menu yang diinginkan di sidebar
3. **Filter Data**: Pilih rentang tanggal dan klik "Filter Data"
4. **Sorting**: Pilih kolom dan urutan sorting
5. **Filter Tambahan**: Gunakan filter kolom spesifik jika diperlukan

## Instalasi

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan aplikasi:
   ```bash
   python app.py
   ```

3. Buka browser dan akses `http://localhost:5000`

## Dependencies

- Flask
- Pandas
- NumPy

## Struktur Modular

Aplikasi menggunakan struktur modular dimana setiap jenis data memiliki handler terpisah:

- **DataHandler**: Handler utama yang mengkoordinasikan semua handler khusus
- **FinancialHandler**: Khusus untuk pemrosesan data keuangan
- **PatientHandler**: Khusus untuk pemrosesan data pasien  
- **SelisihTarifHandler**: Khusus untuk pemrosesan data selisih tarif
- **LOSHandler**: Khusus untuk pemrosesan data LOS (Length of Stay)

Struktur ini memungkinkan:
- Kode yang lebih rapi dan mudah dikelola
- Pemisahan logika bisnis yang jelas
- Kemudahan dalam maintenance dan pengembangan
- Reusability kode yang lebih baik
