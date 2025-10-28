# Admin dan Viewer Roles - Dokumentasi Fitur

## Overview
Sistem telah diperbarui dengan implementasi role-based access control yang memungkinkan pembedaan akses antara Admin, User, dan Viewer.

## Fitur yang Diimplementasikan

### 1. Role Admin
- **Akses Penuh**: Admin memiliki akses ke semua fitur sistem
- **User Management**: 
  - Melihat daftar semua user
  - Reset password user
  - Hapus user (soft delete)
  - Generate kode registrasi
- **Kode Registrasi**:
  - Generate kode untuk role user, viewer, atau admin
  - Set expiry date untuk kode
  - Hapus kode yang belum digunakan

### 2. Role Viewer
- **Akses Terbatas**: Viewer hanya dapat melihat data, tidak dapat mengupload
- **Restrictions**:
  - Tidak dapat mengakses menu "Upload File"
  - Tidak dapat mengupload data baru
  - Hanya dapat melihat dan menganalisis data yang sudah ada

### 3. Role User
- **Akses Standar**: User dapat menggunakan semua fitur kecuali admin functions
- **Permissions**:
  - Upload data
  - Melihat dan menganalisis data
  - Tidak dapat mengakses admin panel

## Struktur Database Baru

### Tabel `registration_codes`
```sql
CREATE TABLE registration_codes (
    code_id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    used_by INTEGER REFERENCES users(user_id),
    used_at TIMESTAMP,
    created_by INTEGER NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## Cara Penggunaan

### 1. Login sebagai Admin
- Username: `admin`
- Password: `admin123`
- Email: `admin@ihc.com`

### 2. Generate Kode Registrasi
1. Login sebagai admin
2. Akses menu "User Management" di sidebar
3. Pilih tab "Kode Registrasi"
4. Klik "Generate Kode"
5. Pilih role (user/viewer/admin)
6. Set expiry date
7. Generate kode

### 3. Registrasi User Baru
1. User baru harus memiliki kode registrasi dari admin
2. Saat registrasi, masukkan kode registrasi
3. Role akan otomatis sesuai dengan kode yang digunakan

### 4. Kode Registrasi Sample
- **User Code**: `9M5YGDBH` (expires in 30 days)
- **Viewer Code**: `EY1WSPTI` (expires in 30 days)  
- **Admin Code**: `IIYGL4G6` (expires in 7 days)

## API Endpoints Baru

### Admin Endpoints
- `GET /admin/users` - Get all users
- `POST /admin/users/{user_id}/reset-password` - Reset user password
- `POST /admin/users/{user_id}/delete` - Delete user
- `GET /admin/registration-codes` - Get all registration codes
- `POST /admin/registration-codes/generate` - Generate new codes
- `POST /admin/registration-codes/{code_id}/delete` - Delete code

### Registration Endpoint (Updated)
- `POST /auth/register` - Register with registration code

## Security Features

### 1. Role-based Access Control
- Setiap endpoint admin memerlukan role admin
- Upload endpoint memblokir role viewer
- UI menyesuaikan berdasarkan role user

### 2. Registration Code System
- Kode registrasi wajib untuk registrasi
- Kode memiliki expiry date
- Kode hanya bisa digunakan sekali
- Role ditentukan oleh kode yang digunakan

### 3. Activity Logging
- Semua aktivitas admin dicatat
- Password reset dicatat
- User deletion dicatat
- Code generation dicatat

## File yang Dimodifikasi

### Backend
- `src/core/database.py` - Added RegistrationCode model
- `src/web/routes.py` - Added admin routes and registration code validation
- `migrations/create_registration_codes_table.sql` - Database migration

### Frontend
- `src/web/templates/index.html` - Added admin section and role-based UI
- `src/web/templates/login.html` - Added registration code field
- `src/web/static/admin.js` - Admin functionality JavaScript
- `src/web/static/login.js` - Updated registration form validation
- `src/web/static/script.js` - Added admin content handling

### Tools
- `tools/create_admin_user.py` - Tool untuk membuat admin user dan sample codes

## Testing

### 1. Test Admin Functions
1. Login sebagai admin
2. Akses User Management
3. Test generate kode registrasi
4. Test reset password user
5. Test hapus user

### 2. Test Viewer Restrictions
1. Registrasi user dengan kode viewer
2. Login sebagai viewer
3. Verifikasi tidak ada menu upload
4. Test akses upload (harus ditolak)

### 3. Test Registration Code System
1. Test registrasi tanpa kode (harus gagal)
2. Test registrasi dengan kode invalid (harus gagal)
3. Test registrasi dengan kode expired (harus gagal)
4. Test registrasi dengan kode valid (harus berhasil)

## Troubleshooting

### 1. Admin User Tidak Ada
```bash
python tools/create_admin_user.py
```

### 2. Database Migration
```bash
# Jalankan migration SQL
psql -h localhost -U postgres -d DAV -f migrations/create_registration_codes_table.sql
```

### 3. Permission Issues
- Pastikan user memiliki role yang tepat
- Check session dan login status
- Verify database connections

## Future Enhancements

### 1. Advanced Permissions
- Granular permissions per feature
- Custom role creation
- Permission inheritance

### 2. Audit Trail
- Detailed activity logs
- User action history
- System change tracking

### 3. Bulk Operations
- Bulk user management
- Bulk code generation
- Import/export user data

## Notes
- Semua kode registrasi sample akan expired sesuai tanggal yang ditentukan
- Admin user default password harus diubah setelah login pertama
- Soft delete untuk user mempertahankan data integrity
- Activity logging membantu monitoring dan debugging




