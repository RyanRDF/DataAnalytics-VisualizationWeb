-- =============================================
-- MIGRATION SCRIPT: Hospital Database Tables
-- Database: DAV (Data Analytics Visualization)
-- Created: $(date)
-- =============================================

-- Menghapus tabel jika sudah ada untuk memungkinkan pembuatan ulang (opsional)
-- HATI-HATI: Script ini akan menghapus data yang ada!
-- Uncomment baris di bawah jika ingin menghapus tabel yang sudah ada
-- DROP TABLE IF EXISTS kunjungan_diagnosa, kunjungan_prosedur, rincian_biaya, kunjungan, pasien, dokter, diagnosa, prosedur;

-- =============================================
-- TABEL MASTER (REFERENSI)
-- =============================================

-- Tabel untuk menyimpan data unik pasien
CREATE TABLE IF NOT EXISTS pasien (
    mrn VARCHAR(20) PRIMARY KEY, -- Medical Record Number, sebagai Primary Key alami
    nama_pasien VARCHAR(255) NOT NULL,
    birth_date DATE,
    sex SMALLINT, -- Menggunakan SMALLINT untuk kode (misal: 1 Laki-laki, 2 Perempuan)
    no_kartu_bpjs VARCHAR(20) UNIQUE,
    umur_tahun INTEGER,
    umur_hari INTEGER
);

-- Tabel untuk menyimpan data dokter
CREATE TABLE IF NOT EXISTS dokter (
    dokter_id SERIAL PRIMARY KEY, -- Menggunakan SERIAL untuk ID auto-increment
    nama_dokter VARCHAR(255) NOT NULL
);

-- Tabel lookup untuk kode diagnosa (ICD-10)
CREATE TABLE IF NOT EXISTS diagnosa (
    kode_diagnosa VARCHAR(10) PRIMARY KEY,
    deskripsi TEXT NOT NULL
);

-- Tabel lookup untuk kode prosedur medis (ICD-9CM)
CREATE TABLE IF NOT EXISTS prosedur (
    kode_prosedur VARCHAR(10) PRIMARY KEY,
    deskripsi TEXT NOT NULL
);

-- =============================================
-- TABEL TRANSAKSI
-- =============================================

-- Tabel utama untuk mencatat setiap kunjungan/rawat inap pasien
CREATE TABLE IF NOT EXISTS kunjungan (
    kunjungan_id SERIAL PRIMARY KEY,
    mrn VARCHAR(20) NOT NULL,
    dokter_id INTEGER,
    admission_date DATE NOT NULL,
    discharge_date DATE,
    los INTEGER, -- Length of Stay (dalam hari)
    kelas_rawat SMALLINT, -- Kode kelas rawat (misal: 1, 2, 3)
    discharge_status VARCHAR(50),
    kode_inacbg VARCHAR(20),
    sep VARCHAR(50), -- Nomor Surat Eligibilitas Peserta
    total_tarif BIGINT DEFAULT 0,
    tarif_rs BIGINT DEFAULT 0,

    -- Mendefinisikan Foreign Keys
    CONSTRAINT fk_kunjungan_pasien FOREIGN KEY(mrn) REFERENCES pasien(mrn),
    CONSTRAINT fk_kunjungan_dokter FOREIGN KEY(dokter_id) REFERENCES dokter(dokter_id)
);

-- Tabel untuk rincian biaya, relasi One-to-One dengan Kunjungan
CREATE TABLE IF NOT EXISTS rincian_biaya (
    rincian_id SERIAL PRIMARY KEY,
    kunjungan_id INTEGER NOT NULL UNIQUE, -- UNIQUE memastikan relasi One-to-One
    prosedur_non_bedah BIGINT DEFAULT 0,
    prosedur_bedah BIGINT DEFAULT 0,
    konsultasi BIGINT DEFAULT 0,
    tenaga_ahli BIGINT DEFAULT 0,
    keperawatan BIGINT DEFAULT 0,
    penunjang BIGINT DEFAULT 0,
    radiologi BIGINT DEFAULT 0,
    laboratorium BIGINT DEFAULT 0,
    pelayanan_darah BIGINT DEFAULT 0,
    kamar_akomodasi BIGINT DEFAULT 0,
    obat BIGINT DEFAULT 0,
    
    -- Mendefinisikan Foreign Key
    CONSTRAINT fk_rincian_kunjungan FOREIGN KEY(kunjungan_id) REFERENCES kunjungan(kunjungan_id) ON DELETE CASCADE -- Data rincian ikut terhapus jika kunjungan dihapus
);

-- =============================================
-- TABEL PENGHUBUNG (MANY-TO-MANY)
-- =============================================

-- Menghubungkan Kunjungan dengan banyak Diagnosa
CREATE TABLE IF NOT EXISTS kunjungan_diagnosa (
    kunjungan_id INTEGER NOT NULL,
    kode_diagnosa VARCHAR(10) NOT NULL,
    
    -- Mendefinisikan Foreign Keys
    CONSTRAINT fk_diag_kunjungan FOREIGN KEY(kunjungan_id) REFERENCES kunjungan(kunjungan_id) ON DELETE CASCADE,
    CONSTRAINT fk_diag_diagnosa FOREIGN KEY(kode_diagnosa) REFERENCES diagnosa(kode_diagnosa),
    
    -- Composite Primary Key untuk memastikan tidak ada duplikasi diagnosa pada kunjungan yang sama
    PRIMARY KEY (kunjungan_id, kode_diagnosa)
);

-- Menghubungkan Kunjungan dengan banyak Prosedur
CREATE TABLE IF NOT EXISTS kunjungan_prosedur (
    kunjungan_id INTEGER NOT NULL,
    kode_prosedur VARCHAR(10) NOT NULL,
    
    -- Mendefinisikan Foreign Keys
    CONSTRAINT fk_proc_kunjungan FOREIGN KEY(kunjungan_id) REFERENCES kunjungan(kunjungan_id) ON DELETE CASCADE,
    CONSTRAINT fk_proc_prosedur FOREIGN KEY(kode_prosedur) REFERENCES prosedur(kode_prosedur),
    
    -- Composite Primary Key
    PRIMARY KEY (kunjungan_id, kode_prosedur)
);

-- =============================================
-- INDEKS (UNTUK PERFORMA KEUERI)
-- =============================================
CREATE INDEX IF NOT EXISTS idx_kunjungan_mrn ON kunjungan(mrn);
CREATE INDEX IF NOT EXISTS idx_kunjungan_admission_date ON kunjungan(admission_date);
CREATE INDEX IF NOT EXISTS idx_kunjungan_discharge_date ON kunjungan(discharge_date);
CREATE INDEX IF NOT EXISTS idx_kunjungan_kode_inacbg ON kunjungan(kode_inacbg);
CREATE INDEX IF NOT EXISTS idx_pasien_no_kartu_bpjs ON pasien(no_kartu_bpjs);
CREATE INDEX IF NOT EXISTS idx_diagnosa_kode ON diagnosa(kode_diagnosa);
CREATE INDEX IF NOT EXISTS idx_prosedur_kode ON prosedur(kode_prosedur);

-- =============================================
-- DATA SAMPLE (OPSIONAL)
-- =============================================

-- Insert sample data untuk testing
INSERT INTO pasien (mrn, nama_pasien, birth_date, sex, no_kartu_bpjs, umur_tahun, umur_hari) VALUES
('MRN001', 'John Doe', '1980-01-15', 1, 'BPJS001', 44, 16000),
('MRN002', 'Jane Smith', '1975-05-20', 2, 'BPJS002', 49, 18000),
('MRN003', 'Bob Johnson', '1990-12-10', 1, 'BPJS003', 34, 12000)
ON CONFLICT (mrn) DO NOTHING;

INSERT INTO dokter (nama_dokter) VALUES
('Dr. Ahmad Wijaya, Sp.PD'),
('Dr. Siti Nurhaliza, Sp.OG'),
('Dr. Budi Santoso, Sp.B')
ON CONFLICT DO NOTHING;

INSERT INTO diagnosa (kode_diagnosa, deskripsi) VALUES
('A09', 'Diare dan gastroenteritis yang diduga berasal dari infeksi'),
('I10', 'Hipertensi esensial (primer)'),
('J18.9', 'Pneumonia, organisme tidak diketahui'),
('K59.0', 'Konstipasi'),
('M79.3', 'Panniculitis, tidak tergolongkan')
ON CONFLICT (kode_diagnosa) DO NOTHING;

INSERT INTO prosedur (kode_prosedur, deskripsi) VALUES
('00.01', 'Injeksi intratekal'),
('00.02', 'Injeksi intraspinal'),
('00.03', 'Injeksi epidural'),
('00.04', 'Injeksi subdural'),
('00.05', 'Injeksi intrakranial')
ON CONFLICT (kode_prosedur) DO NOTHING;

-- =============================================
-- VERIFIKASI TABEL
-- =============================================

-- Menampilkan daftar tabel yang telah dibuat
SELECT table_name, table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('pasien', 'dokter', 'diagnosa', 'prosedur', 'kunjungan', 'rincian_biaya', 'kunjungan_diagnosa', 'kunjungan_prosedur')
ORDER BY table_name;

-- Menampilkan jumlah data sample
SELECT 
    'Pasien' as tabel, COUNT(*) as jumlah FROM pasien
UNION ALL
SELECT 
    'Dokter' as tabel, COUNT(*) as jumlah FROM dokter
UNION ALL
SELECT 
    'Diagnosa' as tabel, COUNT(*) as jumlah FROM diagnosa
UNION ALL
SELECT 
    'Prosedur' as tabel, COUNT(*) as jumlah FROM prosedur;

-- =============================================
-- CATATAN PENTING
-- =============================================

/*
1. Script ini menggunakan CREATE TABLE IF NOT EXISTS untuk menghindari error jika tabel sudah ada
2. Data sample disisipkan dengan ON CONFLICT DO NOTHING untuk menghindari duplikasi
3. Semua constraint dan indeks dibuat dengan IF NOT EXISTS
4. Script ini kompatibel dengan database DAV yang sudah ada
5. Untuk menghapus tabel yang sudah ada, uncomment baris DROP TABLE di atas
6. Pastikan database DAV sudah dibuat dan user postgres memiliki akses
*/
