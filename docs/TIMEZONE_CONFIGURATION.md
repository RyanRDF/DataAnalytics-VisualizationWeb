# Timezone Configuration - Jakarta (UTC+7)

## Overview
Aplikasi telah dikonfigurasi untuk menggunakan timezone Jakarta (UTC+7) sebagai default timezone untuk semua timestamp dan datetime operations.

## Changes Made

### 1. Timezone Utility Functions (`src/utils/timezone_utils.py`)
- **`jakarta_now()`**: Menggantikan `datetime.utcnow()` untuk mendapatkan waktu saat ini dalam Jakarta timezone
- **`utc_to_jakarta(utc_dt)`**: Konversi UTC datetime ke Jakarta timezone
- **`jakarta_to_utc(jakarta_dt)`**: Konversi Jakarta datetime ke UTC
- **`format_jakarta_time(dt, format_str)`**: Format datetime ke string dalam Jakarta timezone

### 2. Database Models (`src/core/database.py`)
Semua default value untuk datetime columns telah diubah dari `datetime.utcnow` ke `jakarta_now`:
- `User.created_at` dan `User.updated_at`
- `UserSession.login_time`
- `UploadLog.upload_time`
- `LoginLog.login_time`
- `DataImportHistory.import_time`
- `UserActivityLog.activity_time`
- `UserRole.created_at`
- `UserRoleAssignment.assigned_at`

### 3. Web Routes (`src/web/routes.py`)
- Login time tracking menggunakan `jakarta_now()`
- Session expiration checking menggunakan `jakarta_now()`
- Logout time tracking menggunakan `jakarta_now()`

### 4. Custom Jinja2 Filters (`src/web/filters.py`)
- **`jakarta_time`**: Format datetime ke string lengkap dalam Jakarta timezone
- **`jakarta_time_short`**: Format datetime ke waktu pendek (HH:MM) dalam Jakarta timezone
- **`jakarta_date`**: Format datetime ke tanggal (YYYY-MM-DD) dalam Jakarta timezone

### 5. Template Updates (`src/web/templates/index.html`)
- Login time display menggunakan filter `jakarta_time_short`
- Semua waktu yang ditampilkan di UI sekarang dalam Jakarta timezone

### 6. Dependencies (`requirements.txt`)
- Menambahkan `pytz` untuk timezone handling

## Usage Examples

### In Python Code
```python
from utils.timezone_utils import jakarta_now, format_jakarta_time

# Get current time in Jakarta
current_time = jakarta_now()

# Format datetime to Jakarta timezone string
formatted_time = format_jakarta_time(some_datetime, '%Y-%m-%d %H:%M:%S')
```

### In Jinja2 Templates
```html
<!-- Display time in Jakarta timezone -->
{{ user_session.login_time | jakarta_time_short }}

<!-- Display full datetime in Jakarta timezone -->
{{ some_datetime | jakarta_time }}

<!-- Display date only in Jakarta timezone -->
{{ some_datetime | jakarta_date }}
```

## Database Considerations

### Existing Data
- Data yang sudah ada di database akan tetap menggunakan UTC timezone
- Untuk menampilkan data lama, sistem akan mengasumsikan data tersebut dalam UTC dan mengkonversi ke Jakarta timezone saat ditampilkan

### New Data
- Semua data baru yang dibuat akan menggunakan Jakarta timezone (UTC+7)
- Timestamp di database akan disimpan dalam format yang kompatibel dengan timezone

## Testing

Untuk memverifikasi bahwa timezone berfungsi dengan benar:

1. **Login ke aplikasi** - Periksa waktu login di sidebar
2. **Upload file** - Periksa timestamp di upload logs
3. **Check database** - Verifikasi bahwa timestamp tersimpan dengan benar

## Notes

- Jakarta timezone (UTC+7) digunakan untuk semua operasi datetime
- Sistem tetap kompatibel dengan data lama yang menggunakan UTC
- Timezone conversion dilakukan secara otomatis saat menampilkan data
- Semua logging dan tracking activity menggunakan Jakarta timezone


