import pandas as pd

class LOSHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def process_los_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process LOS data with required calculations, sorting, and date filtering"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Select required columns
            required_columns = [
                'SEP', 'MRN', 'DIAGLIST', 'PROCLIST', 'INACBG', 'LOS', 'DISCHARGE_STATUS',
                'TOTAL_TARIF', 'TARIF_RS', 'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in self.data_handler.current_df.columns]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            # Create a copy of the dataframe with required columns
            los_df = self.data_handler.current_df[required_columns].copy()
            
            # Process DIAGLIST to extract PDX and SDX
            def extract_diagnosis(diaglist):
                if pd.isna(diaglist) or diaglist == '':
                    return '', ''
                
                diaglist_str = str(diaglist)
                if ';' in diaglist_str:
                    parts = diaglist_str.split(';')
                    pdx = parts[0].strip()
                    sdx = ';'.join(parts[1:]).strip()
                    return pdx, sdx
                else:
                    return diaglist_str.strip(), ''
            
            # Apply diagnosis extraction
            diagnosis_data = los_df['DIAGLIST'].apply(extract_diagnosis)
            los_df['PDX'] = [d[0] for d in diagnosis_data]
            los_df['SDX'] = [d[1] for d in diagnosis_data]
            
            # Process DISCHARGE_STATUS to convert to readable text
            def convert_discharge_status(status):
                if pd.isna(status) or status == '':
                    return ''
                
                status_str = str(status).strip()
                if status_str == '1':
                    return 'Persetujuan Dokter'
                elif status_str == '2':
                    return 'Dirujuk'
                elif status_str == '3':
                    return 'Persetujuan Sendiri'
                elif status_str == '4':
                    return 'Meninggal'
                else:
                    return status_str
            
            # Apply discharge status conversion
            los_df['CARA_PULANG'] = los_df['DISCHARGE_STATUS'].apply(convert_discharge_status)
            
            # Rename columns according to requirements
            los_df = los_df.rename(columns={
                'MRN': 'MRN',
                'TOTAL_TARIF': 'TOTAL_CLAIM',
                'TARIF_RS': 'TOTAL_BILING_RS'
            })
            
            # Calculate SELISIH (TOTAL_CLAIM - TOTAL_BILING_RS)
            los_df['SELISIH'] = los_df['TOTAL_CLAIM'] - los_df['TOTAL_BILING_RS']
            
            # Reorder columns to match the required format
            final_columns = [
                'SEP', 'MRN', 'PDX', 'SDX', 'PROCLIST', 'INACBG', 'LOS', 'CARA_PULANG',
                'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH',
                'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Ensure all columns exist (fill missing ones with empty strings)
            for col in final_columns:
                if col not in los_df.columns:
                    los_df[col] = ''
            
            los_df = los_df[final_columns]
            
            # Convert numeric columns
            numeric_columns = ['LOS', 'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']
            for col in numeric_columns:
                if col in los_df.columns:
                    los_df[col] = pd.to_numeric(los_df[col], errors='coerce').fillna(0)
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    los_df['ADMISSION_DATE_DT'] = pd.to_datetime(los_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        los_df = los_df[los_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        los_df = los_df[los_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    los_df = los_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if los_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Apply sorting if specified
            if sort_column and sort_column in los_df.columns:
                try:
                    # Handle numeric columns for proper sorting
                    if sort_column in ['LOS', 'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']:
                        los_df = los_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        los_df = los_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return los_df, None
            
        except Exception as e:
            return None, f"Error processing LOS data: {str(e)}"
    
    def get_los_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get LOS data as HTML table with sorting and date filtering"""
        los_df, error = self.process_los_data(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = los_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating LOS table: {str(e)}"
    
    def get_los_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get LOS data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base LOS data
            los_df, error = self.process_los_data(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in los_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if los_df[filter_column].dtype == 'object':  # String columns
                        los_df = los_df[
                            los_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                        ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            los_df = los_df[los_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            los_df = los_df[
                                los_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if los_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = los_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered LOS table: {str(e)}"
    
    def get_los_columns(self):
        """Get list of available columns for LOS data sorting and filtering"""
        if self.data_handler.current_df is None:
            return []
        
        try:
            # Get the LOS dataframe to see all available columns
            los_df, error = self.process_los_data()
            if error:
                return []
            
            return list(los_df.columns)
        except Exception as e:
            return []

