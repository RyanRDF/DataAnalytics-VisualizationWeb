# Database Simplification - Focus on DataAnalytics Only

## Overview
Sistem telah disederhanakan untuk fokus hanya pada tabel `data_analytics` saja. Semua tabel lainnya dari `data_import_history` sampai `rumah_sakit` telah dihapus beserta kode dan fungsi yang berhubungan.

## Tables Removed

### Database Models Removed:
1. **DataImportHistory** - Tabel untuk tracking import history
2. **Pasien** - Tabel untuk data pasien
3. **Dokter** - Tabel untuk data dokter
4. **Diagnosa** - Tabel untuk kode diagnosa (ICD-10)
5. **Prosedur** - Tabel untuk kode prosedur medis (ICD-9CM)
6. **Kunjungan** - Tabel utama untuk kunjungan/rawat inap
7. **RincianBiaya** - Tabel untuk rincian biaya
8. **KunjunganDiagnosa** - Tabel relasi kunjungan-diagnosa
9. **KunjunganProsedur** - Tabel relasi kunjungan-prosedur

### Files Removed:
1. **`src/core/data_import_service.py`** - Service untuk import data ke multiple tables
2. **`src/core/flexible_data_extractor.py`** - Extractor yang menggunakan multiple tables

## Tables Kept

### Core Tables:
1. **User** - Tabel untuk user management
2. **UserSession** - Tabel untuk session management
3. **UploadLog** - Tabel untuk tracking upload files
4. **LoginLog** - Tabel untuk tracking login
5. **UserActivityLog** - Tabel untuk tracking user activity
6. **UserRole** - Tabel untuk role management
7. **UserRoleAssignment** - Tabel untuk user-role assignment
8. **DataAnalytics** - Tabel utama untuk data analytics (FOCUS TABLE)

## Code Changes Made

### 1. Database Models (`src/core/database.py`)
- Removed all hospital-related models (Pasien, Dokter, Diagnosa, etc.)
- Removed DataImportHistory model
- Kept only core user management and DataAnalytics models
- Removed relationships to deleted models

### 2. Database Query Service (`src/core/database_query_service.py`)
- **Completely rewritten** to focus only on DataAnalytics table
- All query methods now use DataAnalytics table directly
- Simplified methods:
  - `get_financial_data()` - Query financial data from DataAnalytics
  - `get_inacbg_data()` - Query INACBG analysis from DataAnalytics
  - `get_los_data()` - Query Length of Stay analysis from DataAnalytics
  - `get_ventilator_data()` - Query ventilator usage from DataAnalytics
  - `get_patient_data()` - Query patient data from DataAnalytics
  - `get_tarif_selisih_data()` - Query tariff difference analysis from DataAnalytics
  - `get_database_stats()` - Get statistics from DataAnalytics only
  - `search_pasien()` - Search patients in DataAnalytics
  - `get_kunjungan_by_pasien()` - Get visits by patient from DataAnalytics

### 3. Robust Data Extractor (`src/core/robust_data_extractor.py`)
- Removed all ERD table insertion methods
- Removed methods:
  - `insert_erd_tables()`
  - `insert_pasien_data()`
  - `insert_dokter_data()`
  - `insert_diagnosa_data()`
  - `insert_prosedur_data()`
- Now focuses only on inserting data to DataAnalytics table
- Simplified import process

### 4. Handlers Updated
- **FinancialHandler** - Updated required columns to match DataAnalytics
- **VentilatorHandler** - Updated to use `VENT_HOUR`, `ICU_INDIKATOR`, `ICU_LOS`
- Other handlers already used correct column names

### 5. Routes (`src/web/routes.py`)
- Removed import for DataImportService
- System now uses only RobustDataExtractor

## Data Flow Simplified

### Before (Complex):
```
File Upload → DataImportService → Multiple Tables (Pasien, Dokter, Diagnosa, etc.)
```

### After (Simplified):
```
File Upload → RobustDataExtractor → DataAnalytics Table Only
```

## Benefits of Simplification

1. **Reduced Complexity**: System is now much simpler with only one main data table
2. **Better Performance**: No complex joins between multiple tables
3. **Easier Maintenance**: Less code to maintain and debug
4. **Faster Development**: Focus on one table makes development faster
5. **Data Integrity**: All data in one place reduces data consistency issues

## DataAnalytics Table Structure

The `data_analytics` table contains all necessary fields:
- **Patient Info**: `nama_pasien`, `mrn`, `nokartu`, `birth_date`, `sex`
- **Visit Info**: `sep`, `admission_date`, `discharge_date`, `los`
- **Medical Info**: `diaglist`, `proclist`, `inacbg`, `dpjp`
- **Financial Info**: `total_tarif`, `tarif_rs`, `prosedur_non_bedah`, `prosedur_bedah`, etc.
- **ICU/Ventilator**: `icu_indikator`, `icu_los`, `vent_hour`

## Migration Notes

- **Existing Data**: All existing data in DataAnalytics table remains intact
- **New Uploads**: New file uploads will only insert to DataAnalytics table
- **Duplicate Checking**: Still works based on SEP field in DataAnalytics
- **Analytics**: All analytics functions now query DataAnalytics table directly

## Testing Required

1. **File Upload**: Test uploading the same file twice to verify duplicate detection
2. **Data Display**: Test all analytics views (Financial, INACBG, LOS, Ventilator, etc.)
3. **Search Functions**: Test patient search functionality
4. **Database Stats**: Verify database statistics display correctly
5. **Row Count Display**: Verify row failed/success display in Data Status

## Next Steps

1. Test the simplified system with the provided test file
2. Verify all analytics functions work correctly
3. Test duplicate detection and row counting
4. Ensure Data Status displays correct information


