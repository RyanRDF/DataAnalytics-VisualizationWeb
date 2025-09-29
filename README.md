# 📊 Data Analytics Dashboard

A comprehensive web application for data analytics and visualization with PostgreSQL database integration.

## 🚀 Features

- **User Authentication**: Secure login/register system with PostgreSQL
- **Data Analytics**: Multiple analysis modules (Financial, Patient, LOS, Ventilator, etc.)
- **File Upload**: Process .txt data files with real-time processing
- **Interactive Dashboard**: Modern, responsive web interface
- **Database Integration**: PostgreSQL with SQLAlchemy ORM

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **ORM**: SQLAlchemy
- **Authentication**: Werkzeug Security

## 📋 Prerequisites

- Python 3.7+
- PostgreSQL 12+
- pip

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DataAnalytics-VisualizationWeb
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL Database**
   - Install PostgreSQL
   - Create database named `DAV`
   - Update database credentials in `src/core/database.py`

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open browser: http://localhost:5000
   - Login with: admin@ihc.com / admin123

## 📁 Project Structure

```
DataAnalytics-VisualizationWeb/
├── src/
│   ├── core/           # Core functionality
│   │   ├── database.py # Database models and configuration
│   │   ├── data_handler.py
│   │   └── data_processor.py
│   ├── handlers/       # Data processing handlers
│   ├── utils/          # Utility functions
│   └── web/            # Web application
│       ├── app.py      # Flask app configuration
│       ├── routes.py   # API routes
│       ├── static/     # CSS, JS, images
│       └── templates/  # HTML templates
├── instance/uploads/   # File upload directory
├── requirements.txt    # Python dependencies
└── app.py             # Application entry point
```

## 🗄️ Database Schema

### Tables
- **users**: User accounts and authentication
- **user_sessions**: Session management
- **data_upload_logs**: File upload tracking

## 🔐 Default Credentials

- **Admin User**: admin@ihc.com / admin123
- **Database**: DAV (PostgreSQL)

## 📊 Available Modules

1. **E-Claim**
   - Financial Analysis
   - Patient Data
   - File Upload

2. **Analytics**
   - Selisih Tarif
   - Length of Stay (LOS)
   - Ventilator Analysis

## 🚀 Getting Started

1. Start the application: `python app.py`
2. Open browser: http://localhost:5000
3. Login with admin credentials
4. Upload data files and explore analytics

## 📝 License

This project is licensed under the MIT License.