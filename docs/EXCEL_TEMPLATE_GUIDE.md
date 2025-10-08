# Panduan Template Excel untuk Upload Data

## Format Kolom yang Diperlukan

File Excel (.xlsx atau .xls) yang diupload harus memiliki kolom dengan nama yang sama persis dengan file .txt. Berikut adalah daftar kolom yang diperlukan:

### Kolom Wajib (Required Columns)
- `KODE_RS` - Kode Rumah Sakit
- `KELAS_RS` - Kelas Rumah Sakit  
- `KELAS_RAWAT` - Kelas Rawat
- `KODE_TARIF` - Kode Tarif
- `ADMISSION_DATE` - Tanggal Masuk (format: DD/MM/YYYY atau YYYY-MM-DD)
- `DISCHARGE_DATE` - Tanggal Keluar (format: DD/MM/YYYY atau YYYY-MM-DD)
- `BIRTH_DATE` - Tanggal Lahir (format: DD/MM/YYYY atau YYYY-MM-DD)
- `SEX` - Jenis Kelamin (1=Laki-laki, 2=Perempuan)
- `NAMA_PASIEN` - Nama Pasien
- `MRN` - Medical Record Number
- `DPJP` - Dokter Penanggung Jawab Pasien
- `TOTAL_TARIF` - Total Tarif
- `TARIF_RS` - Tarif Rumah Sakit
- `LOS` - Length of Stay (hari)
- `KODE_INACBG` - Kode INACBG
- `SEP` - Surat Eligibilitas Peserta

### Kolom Opsional (Optional Columns)
- `NOKARTU` - Nomor Kartu BPJS
- `UMUR_TAHUN` - Umur dalam Tahun
- `UMUR_HARI` - Umur dalam Hari
- `DISCHARGE_STATUS` - Status Keluar
- `DIAGLIST` - Daftar Diagnosa (pisahkan dengan ;)
- `PROCLIST` - Daftar Prosedur (pisahkan dengan ;)

### Kolom Rincian Biaya (Optional)
- `PROSEDUR_NON_BEDAH` - Prosedur Non Bedah
- `PROSEDUR_BEDAH` - Prosedur Bedah
- `KONSULTASI` - Konsultasi
- `TENAGA_AHLI` - Tenaga Ahli
- `KEPERAWATAN` - Keperawatan
- `PENUNJANG` - Penunjang
- `RADIOLOGI` - Radiologi
- `LABORATORIUM` - Laboratorium
- `PELAYANAN_DARAH` - Pelayanan Darah
- `KAMAR_AKOMODASI` - Kamar Akomodasi
- `OBAT` - Obat

## Format Data

### Tanggal
- Format yang didukung: DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
- Contoh: 15/01/2024, 2024-01-15, 15-01-2024

### Jenis Kelamin
- 1 = Laki-laki
- 2 = Perempuan

### Diagnosa dan Prosedur
- Jika ada multiple diagnosa/prosedur, pisahkan dengan titik koma (;)
- Contoh: A09;I10;J18.9

### Nilai Numerik
- Gunakan angka tanpa format khusus
- Untuk nilai kosong, biarkan sel kosong atau gunakan 0

## Contoh Template Excel

| MRN | NAMA_PASIEN | BIRTH_DATE | SEX | ADMISSION_DATE | DISCHARGE_DATE | LOS | TOTAL_TARIF | TARIF_RS | DPJP | KODE_INACBG |
|-----|-------------|------------|-----|----------------|----------------|-----|--------------|----------|------|-------------|
| MRN001 | John Doe | 15/01/1980 | 1 | 01/01/2024 | 05/01/2024 | 4 | 5000000 | 4500000 | Dr. Ahmad | 12345 |

## Tips Upload Excel

1. **Pastikan nama kolom sama persis** dengan yang ada di file .txt
2. **Hindari spasi ekstra** di nama kolom
3. **Gunakan format tanggal yang konsisten** dalam satu file
4. **Periksa tipe data** - angka harus berupa angka, bukan teks
5. **Hindari karakter khusus** dalam nama kolom
6. **File Excel akan diproses sama** seperti file .txt dengan format yang sama

## Validasi Data

Sistem akan memvalidasi:
- Keberadaan kolom wajib
- Format tanggal yang valid
- Nilai numerik yang valid
- Tidak ada nilai null pada kolom wajib (MRN, NAMA_PASIEN, ADMISSION_DATE)

Jika ada error, sistem akan menampilkan pesan error yang spesifik untuk membantu perbaikan data.

