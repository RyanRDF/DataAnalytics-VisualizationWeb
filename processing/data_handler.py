import pandas as pd
import numpy as np
import os

class DataHandler:
    def __init__(self):
        self.current_df = None
    
    def load_data_from_file(self, filepath):
        """Load data from uploaded file"""
        try:
            # Read the uploaded file with tab separator
            df = pd.read_csv(filepath, sep='\t')
            self.current_df = df
            return df, None
        except Exception as e:
            return None, f"Error loading file: {str(e)}"
    
    def get_raw_data_table(self):
        """Get raw data as HTML table"""
        if self.current_df is None:
            return "", False
        
        try:
            table_html = self.current_df.to_html(classes='data-table', index=False)
            return table_html, True
        except Exception as e:
            return "", False
    
    def process_patient_data(self):
        """Process patient data with all required columns"""
        if self.current_df is None:
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
            existing_columns = [col for col in patient_columns if col in self.current_df.columns]
            missing_columns = [col for col in patient_columns if col not in self.current_df.columns]
            
            if not existing_columns:
                return None, "No patient-related columns found in the data."
            
            # Create a copy of the dataframe with existing patient columns
            patient_df = self.current_df[existing_columns].copy()
            
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
        if self.current_df is None:
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
        if self.current_df is None:
            return []
        
        try:
            # Get the patient dataframe to see all available columns
            patient_df, error = self.process_patient_data()
            if error:
                return []
            
            return list(patient_df.columns)
        except Exception as e:
            return []
    
    def process_financial_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process financial data with required calculations, sorting, and date filtering"""
        if self.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Select required columns
            required_columns = [
                'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF', 
                'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN', 
                'NOKARTU', 'TOTAL_TARIF', 'TARIF_RS'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in self.current_df.columns]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            # Create a copy of the dataframe with required columns
            financial_df = self.current_df[required_columns].copy()
            
            # Convert LOS to numeric, handling any non-numeric values
            financial_df['LOS'] = pd.to_numeric(financial_df['LOS'], errors='coerce').fillna(0)
            
            # Convert TOTAL_TARIF and TARIF_RS to numeric
            financial_df['TOTAL_TARIF'] = pd.to_numeric(financial_df['TOTAL_TARIF'], errors='coerce').fillna(0)
            financial_df['TARIF_RS'] = pd.to_numeric(financial_df['TARIF_RS'], errors='coerce').fillna(0)
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    financial_df['ADMISSION_DATE_DT'] = pd.to_datetime(financial_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        financial_df = financial_df[financial_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        financial_df = financial_df[financial_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    financial_df = financial_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if financial_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Calculate derived columns
            # TOTAL_TARIF/HARI (TOTAL_TARIF divided by LOS)
            financial_df['TOTAL_TARIF/HARI'] = np.where(
                financial_df['LOS'] > 0, 
                financial_df['TOTAL_TARIF'] / financial_df['LOS'], 
                0
            )
            
            # TARIF_RS/HARI (TARIF_RS divided by LOS)
            financial_df['TARIF_RS/HARI'] = np.where(
                financial_df['LOS'] > 0, 
                financial_df['TARIF_RS'] / financial_df['LOS'], 
                0
            )
            
            # LABA (TOTAL_TARIF - TARIF_RS, if negative then output 0, if positive then show the output as it is)
            financial_df['LABA'] = np.where(
                financial_df['TOTAL_TARIF'] - financial_df['TARIF_RS'] > 0,
                financial_df['TOTAL_TARIF'] - financial_df['TARIF_RS'],
                0
            )
            
            # LABA/HARI (LABA divided by LOS)
            financial_df['LABA/HARI'] = np.where(
                financial_df['LOS'] > 0,
                financial_df['LABA'] / financial_df['LOS'],
                0
            )
            
            # RUGI (TOTAL_TARIF - TARIF_RS, if negative then output is in absolute, if positive then show the output 0)
            financial_df['RUGI'] = np.where(
                financial_df['TOTAL_TARIF'] - financial_df['TARIF_RS'] < 0,
                abs(financial_df['TOTAL_TARIF'] - financial_df['TARIF_RS']),
                0
            )
            
            # RUGI/HARI (RUGI divided by LOS)
            financial_df['RUGI/HARI'] = np.where(
                financial_df['LOS'] > 0,
                financial_df['RUGI'] / financial_df['LOS'],
                0
            )
            
            # Round numeric columns to 2 decimal places
            numeric_columns = ['TOTAL_TARIF/HARI', 'TARIF_RS/HARI', 'LABA', 'LABA/HARI', 'RUGI', 'RUGI/HARI']
            for col in numeric_columns:
                financial_df[col] = financial_df[col].round(2)
            
            # Apply sorting if specified
            if sort_column and sort_column in financial_df.columns:
                try:
                    # Handle numeric columns for proper sorting
                    if sort_column in ['LOS', 'TOTAL_TARIF', 'TARIF_RS', 'TOTAL_TARIF/HARI', 'TARIF_RS/HARI', 'LABA', 'LABA/HARI', 'RUGI', 'RUGI/HARI']:
                        financial_df = financial_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        financial_df = financial_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return financial_df, None
            
        except Exception as e:
            return None, f"Error processing financial data: {str(e)}"
    
    def get_financial_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get financial data as HTML table with sorting and date filtering"""
        financial_df, error = self.process_financial_data(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = financial_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating financial table: {str(e)}"
    
    def get_financial_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get financial data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base financial data
            financial_df, error = self.process_financial_data(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in financial_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if financial_df[filter_column].dtype == 'object':  # String columns
                        financial_df = financial_df[
                            financial_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                        ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            financial_df = financial_df[financial_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            financial_df = financial_df[
                                financial_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if financial_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = financial_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered financial table: {str(e)}"
    
    def get_financial_columns(self):
        """Get list of available columns for financial data sorting"""
        if self.current_df is None:
            return []
        
        try:
            # Get the financial dataframe to see all available columns
            financial_df, error = self.process_financial_data()
            if error:
                return []
            
            return list(financial_df.columns)
        except Exception as e:
            return []
    
    def validate_file(self, filename):
        """Validate uploaded file"""
        if not filename.endswith('.txt'):
            return False, "Please upload a .txt file"
        return True, None
    
    def save_uploaded_file(self, file, upload_folder):
        """Save uploaded file to temporary location"""
        try:
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            return filepath, None
        except Exception as e:
            return None, f"Error saving file: {str(e)}"
    
    def cleanup_file(self, filepath):
        """Clean up uploaded file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            # Could not remove file
            pass
    
    def has_data(self):
        """Check if data is loaded"""
        return self.current_df is not None
