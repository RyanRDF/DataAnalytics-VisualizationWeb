# 📊 Data Analytics Dashboard - Dokumentasi Lengkap

Aplikasi web untuk analisis dan visualisasi data rumah sakit dengan PostgreSQL database.

## 📚 Daftar Isi

### 🏗️ **Arsitektur & Struktur**
- **[DATABASE_SIMPLIFICATION.md](DATABASE_SIMPLIFICATION.md)** - Struktur database dan tabel
- **[REVAMPED_APPLICATION_FLOW.md](REVAMPED_APPLICATION_FLOW.md)** - Alur aplikasi dan arsitektur

### 👥 **User Management**
- **[ADMIN_AND_VIEWER_ROLES.md](ADMIN_AND_VIEWER_ROLES.md)** - Sistem role dan permissions
- **[DELETE_USER_GUIDE.md](DELETE_USER_GUIDE.md)** - Panduan menghapus user
- **[PASSWORD_SECURITY.md](PASSWORD_SECURITY.md)** - Keamanan password

### 📤 **Upload & Data Processing**
- **[NEW_UPLOAD水晶stem.md](NEW_UPLOAD水晶stem.md)** - Sistem upload file baru
- **[EXCEL_TEMPLATE_GUIDE.md](EXCEL_TEMPLATE_GUIDE.md)** - Template Excel untuk upload
- **[EXCEL_TROUBLESHOOTING.md](EXCEL_TROUBLESHOOTING.md)** - Troubleshooting masalah upload
- **[INACBG_PRICING_ADJUSTMENTS.md](INACBG_PRICING_ADJUSTMENTS.md)** - Penyesuaian harga INACBG

### 🔧 **Konfigurasi & Maintenance**
- **[TIMEZONE_CONFIGURATION.md](TIMEZONE_CONFIGURATION.md)** - Konfigurasi timezone Jakarta
- **[PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)** - Optimasi performa
- **[CLEAR_TABLES_GUIDE.md](CLEAR_TABLES_GUIDE.md)** - Panduan membersihkan tabel data

### 📝 **Fixes & Improvements**
- **[FIXES_AND_IMPROVEMENTS.md](FIXES_AND_IMPROVEMENTS.md)** - Daftar perbaikan dan peningkatan

### 🧹 **Project Cleanup**
- **[PROJECT_CLEANUP_FINAL.md完整性** - Summary final cleanup project

---

## 🚀 Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Setup database PostgreSQL
3. Run: `python app.py`
4. Access: http://localhost:5000
5. Login: admin@ihc.com / admin123

## 📊 Database Structure

### Core Tables (7):
1. `data_analytics` - Main data table
2. `users` - User management
3. `user_sessions` - Session management
4. `upload_logs` - Upload tracking
5. `login_logs` - Login tracking
6. `user_activity_logs` - Activity tracking
7. `registration_codes` - Registration codes

## 🔐 Features

- ✅ Role-based access control (Admin, User, Viewer)
- ✅ File upload & data processing
- ✅ Multiple analytics views (Financial, Patient, LOS, Ventilator, INACBG)
- ✅ Interactive filtering and sorting
- ✅ User management & activity logging
- ✅ Secure session management

---

*Last Updated: Project Cleanup Complete*

