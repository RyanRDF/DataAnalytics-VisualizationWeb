import pandas as pd

def format_rupiah(value):
    """Format numeric value to Indonesian Rupiah format (Rp. 1.000.000)"""
    if pd.isna(value) or value == 0 or value == '' or value is None:
        return "Rp. 0"
    
    try:
        # Convert to integer to remove decimals
        int_value = int(float(value))
        
        # Format with thousand separators
        formatted = f"{int_value:,}".replace(",", ".")
        
        return f"Rp. {formatted}"
    except (ValueError, TypeError):
        return "Rp. 0"

class SelisihTarifHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def process_selisih_tarif_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process selisih tarif data with required calculations, sorting, and date filtering"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Select required columns
            required_columns = [
                'SEP', 'MRN', 'LOS', 'DIAGLIST', 'PROCLIST', 'INACBG', 'DESKRIPSI_INACBG',
                'TOTAL_TARIF', 'TARIF_RS', 'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in self.data_handler.current_df.columns]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            # Create a copy of the dataframe with required columns
            selisih_df = self.data_handler.current_df[required_columns].copy()
            
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
            diagnosis_data = selisih_df['DIAGLIST'].apply(extract_diagnosis)
            selisih_df['PDX'] = [d[0] for d in diagnosis_data]
            selisih_df['SDX'] = [d[1] for d in diagnosis_data]
            
            # Rename columns according to requirements
            selisih_df = selisih_df.rename(columns={
                'MRN': 'RM',
                'TOTAL_TARIF': 'TOTAL_CLAIM',
                'TARIF_RS': 'TOTAL_BILING_RS'
            })
            
            # Calculate SELISIH (TOTAL_CLAIM - TOTAL_BILING_RS)
            selisih_df['SELISIH'] = selisih_df['TOTAL_CLAIM'] - selisih_df['TOTAL_BILING_RS']
            
            # Reorder columns to match the required format
            final_columns = [
                'SEP', 'RM', 'LOS', 'PDX', 'SDX', 'PROCLIST', 'INACBG', 
                'DESKRIPSI_INACBG', 'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH',
                'ADMISSION_DATE', 'DISCHARGE_DATE'
            ]
            
            # Ensure all columns exist (fill missing ones with empty strings)
            for col in final_columns:
                if col not in selisih_df.columns:
                    selisih_df[col] = ''
            
            selisih_df = selisih_df[final_columns]
            
            # Convert numeric columns
            numeric_columns = ['LOS', 'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']
            for col in numeric_columns:
                if col in selisih_df.columns:
                    selisih_df[col] = pd.to_numeric(selisih_df[col], errors='coerce').fillna(0)
            
            # Format financial columns to Indonesian Rupiah format
            financial_columns = ['TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']
            for col in financial_columns:
                if col in selisih_df.columns:
                    selisih_df[col] = selisih_df[col].apply(format_rupiah)
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    selisih_df['ADMISSION_DATE_DT'] = pd.to_datetime(selisih_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        selisih_df = selisih_df[selisih_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        selisih_df = selisih_df[selisih_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    selisih_df = selisih_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if selisih_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Apply sorting if specified
            if sort_column and sort_column in selisih_df.columns:
                try:
                    # Handle numeric columns for proper sorting
                    if sort_column in ['LOS', 'TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']:
                        # For financial columns that are now formatted as strings, we need to sort by the original numeric values
                        if sort_column in ['TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']:
                            # Create temporary numeric columns for sorting
                            temp_col = f"{sort_column}_NUM"
                            selisih_df[temp_col] = selisih_df[sort_column].str.replace('Rp. ', '').str.replace('.', '').astype(float)
                            selisih_df = selisih_df.sort_values(by=temp_col, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                            selisih_df = selisih_df.drop(temp_col, axis=1)
                        else:
                            selisih_df = selisih_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        selisih_df = selisih_df.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return selisih_df, None
            
        except Exception as e:
            return None, f"Error processing selisih tarif data: {str(e)}"
    
    def get_selisih_tarif_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get selisih tarif data as HTML table with sorting and date filtering"""
        selisih_df, error = self.process_selisih_tarif_data(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = selisih_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating selisih tarif table: {str(e)}"
    
    def get_selisih_tarif_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get selisih tarif data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base selisih tarif data
            selisih_df, error = self.process_selisih_tarif_data(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in selisih_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if selisih_df[filter_column].dtype == 'object':  # String columns
                        # Check if it's a formatted financial column
                        if filter_column in ['TOTAL_CLAIM', 'TOTAL_BILING_RS', 'SELISIH']:
                            # For financial columns, try to match the formatted value or numeric value
                            try:
                                # Try to convert filter value to numeric and format it
                                numeric_value = float(filter_value)
                                formatted_value = format_rupiah(numeric_value)
                                selisih_df = selisih_df[selisih_df[filter_column] == formatted_value]
                            except ValueError:
                                # If conversion fails, try string search
                                selisih_df = selisih_df[
                                    selisih_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                                ]
                        else:
                            # Regular string search
                            selisih_df = selisih_df[
                                selisih_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            selisih_df = selisih_df[selisih_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            selisih_df = selisih_df[
                                selisih_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if selisih_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = selisih_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered selisih tarif table: {str(e)}"
    
    def get_selisih_tarif_columns(self):
        """Get list of available columns for selisih tarif data sorting and filtering"""
        if self.data_handler.current_df is None:
            return []
        
        try:
            # Get the selisih tarif dataframe to see all available columns
            selisih_df, error = self.process_selisih_tarif_data()
            if error:
                return []
            
            return list(selisih_df.columns)
        except Exception as e:
            return []
