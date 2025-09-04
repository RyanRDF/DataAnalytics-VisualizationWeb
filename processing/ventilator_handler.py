import pandas as pd
import json
import numpy as np

class VentilatorHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def process_ventilator_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process ventilator data with required calculations, sorting, and date filtering"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Select required columns
            required_columns = [
                'SEP', 'MRN', 'LOS', 'DIAGLIST', 'PROCLIST', 'C2', 
                'TOTAL_TARIF', 'TARIF_RS', 'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in self.data_handler.current_df.columns]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            # Create a copy of the dataframe with required columns
            ventilator_df = self.data_handler.current_df[required_columns].copy()
            
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
            diagnosis_data = ventilator_df['DIAGLIST'].apply(extract_diagnosis)
            ventilator_df['PDX'] = [d[0] for d in diagnosis_data]
            ventilator_df['SDX'] = [d[1] for d in diagnosis_data]
            
            # Process C2 column to extract ventilator data
            def extract_ventilator_data(c2_data):
                if pd.isna(c2_data) or c2_data == '':
                    return 'Tidak Pakai Vent', 0
                
                try:
                    # Parse JSON data from C2 column
                    c2_str = str(c2_data)
                    if c2_str.startswith('{') and c2_str.endswith('}'):
                        # Extract ventilator data from JSON
                        if '"ventilator":' in c2_str:
                            # Find ventilator section
                            start_idx = c2_str.find('"ventilator":')
                            if start_idx != -1:
                                # Find the end of ventilator object
                                brace_count = 0
                                start_brace = c2_str.find('{', start_idx)
                                if start_brace != -1:
                                    for i in range(start_brace, len(c2_str)):
                                        if c2_str[i] == '{':
                                            brace_count += 1
                                        elif c2_str[i] == '}':
                                            brace_count -= 1
                                            if brace_count == 0:
                                                end_brace = i
                                                break
                                    
                                    ventilator_json = c2_str[start_brace:end_brace + 1]
                                    ventilator_data = json.loads(ventilator_json)
                                    
                                    use_ind = ventilator_data.get('use_ind', '0')
                                    start_dttm = ventilator_data.get('start_dttm', '0000-00-00 00:00:00')
                                    stop_dttm = ventilator_data.get('stop_dttm', '0000-00-00 00:00:00')
                                    
                                    if use_ind == '1':
                                        # Calculate ventilator hours
                                        try:
                                            if start_dttm != '0000-00-00 00:00:00' and stop_dttm != '0000-00-00 00:00:00':
                                                start_dt = pd.to_datetime(start_dttm)
                                                stop_dt = pd.to_datetime(stop_dttm)
                                                vent_hours = (stop_dt - start_dt).total_seconds() / 3600
                                                return 'Pakai Vent', max(0, vent_hours)
                                            else:
                                                return 'Pakai Vent', 0
                                        except:
                                            return 'Pakai Vent', 0
                                    else:
                                        return 'Tidak Pakai Vent', 0
                    
                    # Fallback: check for use_ind pattern in the string
                    if '"use_ind":"1"' in c2_str:
                        return 'Pakai Vent', 0
                    elif '"use_ind":"0"' in c2_str:
                        return 'Tidak Pakai Vent', 0
                    else:
                        return 'Tidak Pakai Vent', 0
                        
                except Exception as e:
                    # If parsing fails, default to no ventilator
                    return 'Tidak Pakai Vent', 0
            
            # Apply ventilator data extraction
            ventilator_data = ventilator_df['C2'].apply(extract_ventilator_data)
            ventilator_df['VENT_USE'] = [d[0] for d in ventilator_data]
            ventilator_df['VENT_HOUR'] = [d[1] for d in ventilator_data]
            
            # Rename columns according to requirements
            ventilator_df = ventilator_df.rename(columns={
                'MRN': 'MR',
                'TOTAL_TARIF': 'TOTAL_CLAIM',
                'TARIF_RS': 'TOTAL_BILLING_RS'
            })
            
            # Calculate SELISIH (TOTAL_CLAIM - TOTAL_BILLING_RS)
            ventilator_df['SELISIH'] = ventilator_df['TOTAL_CLAIM'] - ventilator_df['TOTAL_BILLING_RS']
            
            # Reorder columns to match the required format
            final_columns = [
                'SEP', 'MR', 'LOS', 'PDX', 'SDX', 'PROCLIST', 'VENT_USE', 'VENT_HOUR',
                'TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH',
                'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Ensure all columns exist (fill missing ones with empty strings)
            for col in final_columns:
                if col not in ventilator_df.columns:
                    ventilator_df[col] = ''
            
            ventilator_df = ventilator_df[final_columns]
            
            # Convert numeric columns
            numeric_columns = ['LOS', 'VENT_HOUR', 'TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH']
            for col in numeric_columns:
                if col in ventilator_df.columns:
                    ventilator_df[col] = pd.to_numeric(ventilator_df[col], errors='coerce').fillna(0)
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    ventilator_df['ADMISSION_DATE_DT'] = pd.to_datetime(ventilator_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        ventilator_df = ventilator_df[ventilator_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        ventilator_df = ventilator_df[ventilator_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    ventilator_df = ventilator_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if ventilator_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Apply sorting if specified
            if sort_column and sort_column in ventilator_df.columns:
                try:
                    # Handle numeric columns for proper sorting
                    if sort_column in ['LOS', 'VENT_HOUR', 'TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH']:
                        ventilator_df = ventilator_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        ventilator_df = ventilator_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return ventilator_df, None
            
        except Exception as e:
            return None, f"Error processing ventilator data: {str(e)}"
    
    def get_ventilator_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get ventilator data as HTML table with sorting and date filtering"""
        ventilator_df, error = self.process_ventilator_data(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = ventilator_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating ventilator table: {str(e)}"
    
    def get_ventilator_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get ventilator data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base ventilator data
            ventilator_df, error = self.process_ventilator_data(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in ventilator_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if ventilator_df[filter_column].dtype == 'object':  # String columns
                        ventilator_df = ventilator_df[
                            ventilator_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                        ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            ventilator_df = ventilator_df[ventilator_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            ventilator_df = ventilator_df[
                                ventilator_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if ventilator_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = ventilator_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered ventilator table: {str(e)}"
    
    def get_ventilator_columns(self):
        """Get list of available columns for ventilator data sorting and filtering"""
        if self.data_handler.current_df is None:
            return []
        
        try:
            # Get the ventilator dataframe to see all available columns
            ventilator_df, error = self.process_ventilator_data()
            if error:
                return []
            
            return list(ventilator_df.columns)
        except Exception as e:
            return []
