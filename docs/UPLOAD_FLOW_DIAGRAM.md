# Diagram Alur Upload System Baru

## Alur Upload Lengkap

```
┌─────────────────┐
│   User Upload   │
│      File       │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ FileAnalyzer    │
│ - analyze_file()│
│ - detect type   │
│ - check support │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ DataExtractor   │
│ - extract_data()│
│ - txt/xlsx      │
│ - clean data    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│DataFrameManager │
│ - set_dataframe()│
│ - validate()    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│DuplicateChecker │
│ - get_existing_ │
│   seps()        │
│ - check_dupl()  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│DataFrameManager │
│ - separate_     │
│   valid_dupl()  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  UploadService  │
│ - upload_valid_ │
│   data()        │
│ - log_upload()  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│DataFrameManager │
│ - clear_        │
│   dataframe()   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Update UI     │
│ - show results  │
│ - rows_success  │
│ - rows_failed   │
└─────────────────┘
```

## Komponen dan Fungsinya

### 1. FileAnalyzer
```
Input: file_path
Output: file_info
- file_type: 'excel' | 'text'
- is_supported: boolean
- encoding: string (untuk text)
- error: string (jika ada)
```

### 2. DataExtractor
```
Input: file_path, file_info
Output: DataFrame, extraction_info
- extract_excel(): untuk file .xlsx/.xls
- extract_text(): untuk file .txt
- clean_dataframe(): bersihkan data
```

### 3. DataFrameManager
```
Input: DataFrame
Output: management_info
- set_dataframe(): set DataFrame
- validate_dataframe(): validasi data
- separate_valid_duplicate_data(): pisahkan data
- clear_dataframe(): bersihkan setelah upload
```

### 4. DuplicateChecker
```
Input: DataFrame
Output: duplicate_info
- get_existing_seps(): ambil SEP dari DB
- check_duplicates(): cek duplikasi
- get_duplicate_details(): detail duplikasi
```

### 5. UploadService
```
Input: file_path, user_id
Output: upload_result
- process_upload(): alur utama
- _upload_valid_data(): upload ke DB
- _log_upload(): log ke upload_logs
- _generate_message(): pesan hasil
```

## Data Flow

### Input Data
```
File (txt/xlsx) → DataFrame → Valid Data + Duplicate Data
```

### Database Operations
```
Valid Data → DataAnalytics Table
Upload Info → UploadLog Table
```

### UI Updates
```
Upload Result → JavaScript → Data Status Display
```

## Error Handling

```
┌─────────────────┐
│   File Error    │
│ - Not supported │
│ - Corrupted     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Extraction Error│
│ - Wrong format  │
│ - Empty file    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Validation Error│
│ - Missing SEP   │
│ - Invalid data  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Upload Error    │
│ - DB connection │
│ - Insert failed │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Show Error    │
│   to User       │
└─────────────────┘
```

## Success Flow

```
┌─────────────────┐
│   All Steps     │
│   Successful    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Update Database │
│ - Insert data   │
│ - Log upload    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Update UI       │
│ - Rows Success  │
│ - Rows Failed   │
│ - Status Color  │
└─────────────────┘
```

## Database Schema

### UploadLog Table
```sql
CREATE TABLE upload_logs (
    upload_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    filename VARCHAR(255),
    file_size BIGINT,
    file_type VARCHAR(50),
    upload_time TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'processing',
    rows_processed INTEGER DEFAULT 0,
    rows_success INTEGER DEFAULT 0,    -- NEW
    rows_failed INTEGER DEFAULT 0,     -- NEW
    error_message TEXT,
    processing_time_seconds INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    file_path VARCHAR(500)
);
```

### DataAnalytics Table
```sql
-- Existing table, no changes needed
-- Used for storing the actual data
```

## Testing Scenarios

### 1. First Upload (New Data)
```
Input: P.04092025_data_ujicoba_apps_analisa.txt
Expected: Rows Success: 18, Rows Failed: 0
```

### 2. Second Upload (Duplicate Data)
```
Input: Same file
Expected: Rows Success: 0, Rows Failed: 18
```

### 3. Mixed Upload (Some New, Some Duplicate)
```
Input: File with 10 new + 8 duplicate rows
Expected: Rows Success: 10, Rows Failed: 8
```

### 4. Excel File Upload
```
Input: .xlsx file
Expected: Same behavior as text file
```

### 5. Error Scenarios
```
Input: Corrupted file
Expected: Error message, no data uploaded
```

