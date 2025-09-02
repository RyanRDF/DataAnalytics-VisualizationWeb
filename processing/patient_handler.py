import pandas as pd

class PatientHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def process_patient_data(self):
        """Process patient data with all required columns"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Define all patient-related columns
            patient_columns = [
                'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF',
                'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN',
                'NOKARTU', 'BIRTH_DATE', 'BIRTH_WEIGHT', 'SEX',
                'DISCHARGE_STATUS', 'DIAGLIST', 'PROCLIST', 'ADL1', 'ADL2',
                'IN_SP', 'IN_SR', 'IN_SI', 'IN_SD', 'INACBG', 'SUBACUTE',
                'CHRONIC', 'SP', 'SR', 'SI', 'SD', 'DESKRIPSI_INACBG',
                'MRN', 'UMUR_TAHUN', 'UMUR_HARI', 'DPJP', 'SEP', 'PAYOR_ID',
                'CODER_ID', 'VERSI_INACBG', 'VERSI_GROUPER'
            ]
            
            # Check which columns exist in the data
            existing_columns = [col for col in patient_columns if col in self.data_handler.current_df.columns]
            missing_columns = [col for col in patient_columns if col not in self.data_handler.current_df.columns]
            
            if not existing_columns:
                return None, "No patient-related columns found in the data."
            
            # Create a copy of the dataframe with existing patient columns
            patient_df = self.data_handler.current_df[existing_columns].copy()
            
            # Fill missing columns with empty values
            for col in missing_columns:
                patient_df[col] = ''
            
            # Reorder columns to match the expected format
            final_columns = patient_columns
            patient_df = patient_df.reindex(columns=final_columns)
            
            # Clean up data - replace None values with empty strings
            patient_df = patient_df.fillna('')
            
            return patient_df, None
            
        except Exception as e:
            return None, f"Error processing patient data: {str(e)}"
    
    def get_patient_table(self):
        """Get patient data as HTML table"""
        patient_df, error = self.process_patient_data()
        
        if error:
            return "", error
        
        try:
            table_html = patient_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating patient table: {str(e)}"
    
    def process_patient_data_with_filters(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process patient data with sorting and date filtering"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Get base patient data
            patient_df, error = self.process_patient_data()
            if error:
                return None, error
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    patient_df['ADMISSION_DATE_DT'] = pd.to_datetime(patient_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        patient_df = patient_df[patient_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        patient_df = patient_df[patient_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    patient_df = patient_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if patient_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Apply sorting if specified
            if sort_column and sort_column in patient_df.columns:
                try:
                    # Handle numeric columns for proper sorting
                    numeric_columns = ['LOS', 'BIRTH_WEIGHT', 'UMUR_TAHUN', 'UMUR_HARI']
                    if sort_column in numeric_columns:
                        # Convert to numeric for proper sorting
                        patient_df[sort_column] = pd.to_numeric(patient_df[sort_column], errors='coerce')
                        patient_df = patient_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        patient_df = patient_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return patient_df, None
            
        except Exception as e:
            return None, f"Error processing patient data with filters: {str(e)}"
    
    def get_patient_table_with_filters(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get patient data as HTML table with sorting and date filtering"""
        patient_df, error = self.process_patient_data_with_filters(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = patient_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating patient table: {str(e)}"
    
    def get_patient_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get patient data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base patient data with filters
            patient_df, error = self.process_patient_data_with_filters(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in patient_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if patient_df[filter_column].dtype == 'object':  # String columns
                        patient_df = patient_df[
                            patient_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                        ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            patient_df = patient_df[patient_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            patient_df = patient_df[
                                patient_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if patient_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = patient_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered patient table: {str(e)}"
    
    def get_patient_columns(self):
        """Get list of available columns for patient data sorting and filtering"""
        if self.data_handler.current_df is None:
            return []
        
        try:
            # Get the patient dataframe to see all available columns
            patient_df, error = self.process_patient_data()
            if error:
                return []
            
            return list(patient_df.columns)
        except Exception as e:
            return []
