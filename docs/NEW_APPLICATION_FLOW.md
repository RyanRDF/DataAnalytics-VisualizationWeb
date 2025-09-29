# 🔄 New Application Flow - DAV Project

## 📋 **Current Flow (Old)**
```
File Upload → DataHandler (Memory) → Handlers → Display
```

## 🎯 **New Flow (Revamped)**
```
File Upload → Database Import → Database Query → Handlers → Display
```

## 🏗️ **Architecture Changes**

### **1. Data Import Service**
- Import data from uploaded files to database
- Parse and validate data before storing
- Handle batch imports and data updates

### **2. Database Query Service**
- Query data directly from database
- Support filtering, sorting, and pagination
- Optimize queries for performance

### **3. Updated Handlers**
- Handlers query from database instead of memory
- Support real-time data analysis
- Maintain data consistency

## 📊 **Database Schema Mapping**

### **File Columns → Database Tables**
```
File Data → Hospital Database Tables
├── KODE_RS, KELAS_RS, KELAS_RAWAT → Kunjungan
├── ADMISSION_DATE, DISCHARGE_DATE, LOS → Kunjungan
├── NAMA_PASIEN, MRN, BIRTH_DATE, SEX → Pasien
├── DPJP → Dokter
├── DIAGLIST → KunjunganDiagnosa + Diagnosa
├── PROCLIST → KunjunganProsedur + Prosedur
├── TOTAL_TARIF, TARIF_RS → Kunjungan
├── PROSEDUR_NON_BEDAH, PROSEDUR_BEDAH, etc. → RincianBiaya
└── KODE_INACBG, SEP → Kunjungan
```

## 🔧 **Implementation Plan**

### **Phase 1: Data Import Service**
1. Create `DataImportService` class
2. Implement file parsing and validation
3. Map file data to database models
4. Handle batch imports and updates

### **Phase 2: Database Query Service**
1. Create `DatabaseQueryService` class
2. Implement query methods for each handler
3. Add filtering and sorting capabilities
4. Optimize query performance

### **Phase 3: Update Handlers**
1. Modify handlers to use database queries
2. Update base handler for database operations
3. Maintain backward compatibility
4. Add error handling

### **Phase 4: Update Routes**
1. Modify upload route to import to database
2. Update analysis routes to query database
3. Add database status endpoints
4. Implement data management features

## 📈 **Benefits of New Flow**

### **1. Data Persistence**
- Data survives application restarts
- Multiple users can access same data
- Historical data analysis

### **2. Performance**
- Database indexing for fast queries
- Efficient filtering and sorting
- Reduced memory usage

### **3. Scalability**
- Handle large datasets
- Support concurrent users
- Easy data backup and restore

### **4. Data Integrity**
- Foreign key constraints
- Data validation
- Consistent data structure

## 🚀 **New User Experience**

### **1. File Upload**
```
User uploads file → Data imported to database → Success message
```

### **2. Data Analysis**
```
User selects analysis → Query database → Display results
```

### **3. Data Management**
```
User can view, filter, sort, and manage data from database
```

## 🔍 **Technical Implementation**

### **Data Import Service**
```python
class DataImportService:
    def import_file_to_database(self, filepath: str) -> ImportResult
    def validate_file_data(self, df: pd.DataFrame) -> ValidationResult
    def map_to_database_models(self, df: pd.DataFrame) -> DatabaseModels
    def batch_insert_data(self, models: List[DatabaseModels]) -> InsertResult
```

### **Database Query Service**
```python
class DatabaseQueryService:
    def get_financial_data(self, filters: Dict) -> pd.DataFrame
    def get_patient_data(self, filters: Dict) -> pd.DataFrame
    def get_los_data(self, filters: Dict) -> pd.DataFrame
    def get_inacbg_data(self, filters: Dict) -> pd.DataFrame
    def get_ventilator_data(self, filters: Dict) -> pd.DataFrame
    def get_selisih_tarif_data(self, filters: Dict) -> pd.DataFrame
```

### **Updated Handlers**
```python
class FinancialHandler(BaseHandler):
    def _query_database(self, filters: Dict) -> pd.DataFrame
    def _process_database_data(self, df: pd.DataFrame) -> pd.DataFrame
    def get_table(self, **kwargs) -> Tuple[str, Optional[str]]
```

## 📋 **Migration Strategy**

### **1. Backward Compatibility**
- Keep existing handlers working
- Gradual migration to database
- Fallback to memory if needed

### **2. Data Migration**
- Import existing data to database
- Validate data integrity
- Test all functionality

### **3. Performance Testing**
- Test with large datasets
- Optimize slow queries
- Monitor memory usage

## 🎯 **Success Metrics**

1. **Data Import**: Successfully import files to database
2. **Query Performance**: Fast response times for analysis
3. **Data Accuracy**: Consistent results between old and new flow
4. **User Experience**: Seamless transition for users
5. **System Stability**: No crashes or data loss

## 🔗 **Related Files**

- `src/core/data_import_service.py` (New)
- `src/core/database_query_service.py` (New)
- `src/core/data_handler.py` (Updated)
- `src/core/base_handler.py` (Updated)
- `src/handlers/*.py` (Updated)
- `src/web/routes.py` (Updated)
