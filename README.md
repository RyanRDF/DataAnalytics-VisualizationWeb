# Data Analytics Visualization Web Application

A Flask-based web application for analyzing and visualizing healthcare data from E-Claim systems. This application provides comprehensive data analysis capabilities for both financial and patient data.

## Features

### 📊 Data Analysis
- **Financial Analysis**: Calculate profit/loss, daily rates, and financial metrics
- **Patient Analysis**: Comprehensive patient data analysis with medical information
- **File Upload**: Support for .txt file uploads with tab-separated data
- **Advanced Filtering**: Date range filtering, column-specific filtering, and sorting

### 🔍 Filtering & Sorting
- Date range filtering for admission dates
- Column-based sorting (ASC/DESC)
- Specific value filtering with case-insensitive search
- Combined filtering and sorting capabilities

### 💻 User Interface
- Modern, responsive web interface
- Interactive sidebar navigation
- Real-time data updates via AJAX
- Clean and intuitive user experience

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DataAnalytics-VisualizationWeb
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Dependencies

- **Flask**: Web framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

## Usage

### 1. Upload Data
- Click "Upload .txt File" in the sidebar
- Select a .txt file with tab-separated data
- Click "Process File" to load the data

### 2. Financial Analysis
- Navigate to "E-Claim > Keuangan"
- Set date range filters
- Apply sorting by any column
- Use specific filters to search for particular values

### 3. Patient Analysis
- Navigate to "E-Claim > Pasien"
- Apply similar filtering and sorting options
- Analyze patient demographics and medical data

## Data Format

The application expects .txt files with tab-separated values containing the following columns:

### Financial Data Columns
- `KODE_RS`, `KELAS_RS`, `KELAS_RAWAT`
- `ADMISSION_DATE`, `DISCHARGE_DATE`, `LOS`
- `TOTAL_TARIF`, `TARIF_RS`
- Additional patient identification columns

### Patient Data Columns
- Patient demographics and medical information
- Admission and discharge details
- Medical procedures and diagnoses
- Length of stay and status information

## Project Structure

```
DataAnalytics-VisualizationWeb/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── processing/
│   └── data_handler.py   # Data processing logic
├── static/
│   ├── script.js         # Frontend JavaScript
│   └── style.css         # Styling
├── templates/
│   └── index.html        # Main HTML template
└── instance/uploads/      # File upload directory
```

## API Endpoints

### Financial Data
- `GET /keuangan` - Display financial analysis
- `GET /keuangan/sort` - Sort financial data
- `GET /keuangan/filter` - Filter financial data by date
- `GET /keuangan/specific-filter` - Filter by specific column values
- `GET /keuangan/columns` - Get available columns

### Patient Data
- `GET /pasien` - Display patient analysis
- `GET /pasien/sort` - Sort patient data
- `GET /pasien/filter` - Filter patient data by date
- `GET /pasien/specific-filter` - Filter by specific column values
- `GET /pasien/columns` - Get available columns

### File Upload
- `POST /upload` - Upload and process data files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or support, please open an issue in the repository.
