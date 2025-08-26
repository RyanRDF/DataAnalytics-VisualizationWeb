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
    
    def process_financial_data(self):
        """Process financial data with required calculations"""
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
            
            return financial_df, None
            
        except Exception as e:
            return None, f"Error processing financial data: {str(e)}"
    
    def get_financial_table(self):
        """Get financial data as HTML table"""
        financial_df, error = self.process_financial_data()
        
        if error:
            return "", error
        
        try:
            table_html = financial_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating financial table: {str(e)}"
    
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
            print(f"Warning: Could not remove file {filepath}: {str(e)}")
    
    def has_data(self):
        """Check if data is loaded"""
        return self.current_df is not None
