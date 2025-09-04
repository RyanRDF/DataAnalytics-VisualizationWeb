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

class INACBGHandler:
    def __init__(self, data_handler):
        self.data_handler = data_handler
    
    def process_inacbg_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Process INACBG data with grouping and aggregation"""
        if self.data_handler.current_df is None:
            return None, "No data available. Please upload a file first."
        
        try:
            # Select required columns
            required_columns = [
                'INACBG', 'LOS', 'TOTAL_TARIF', 'TARIF_RS', 'ADMISSION_DATE'
            ]
            
            # Check if all required columns exist
            missing_columns = [col for col in required_columns if col not in self.data_handler.current_df.columns]
            if missing_columns:
                return None, f"Missing columns: {', '.join(missing_columns)}"
            
            # Create a copy of the dataframe with required columns
            inacbg_df = self.data_handler.current_df[required_columns].copy()
            
            # Apply date filtering if specified (handle DD/MM/YYYY format from data)
            if start_date or end_date:
                try:
                    # Convert input dates (YYYY-MM-DD) to datetime for comparison
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                    
                    # Convert ADMISSION_DATE to datetime for proper comparison
                    inacbg_df['ADMISSION_DATE_DT'] = pd.to_datetime(inacbg_df['ADMISSION_DATE'], format='%d/%m/%Y', errors='coerce')
                    
                    # Apply start date filter
                    if start_date:
                        inacbg_df = inacbg_df[inacbg_df['ADMISSION_DATE_DT'] >= start_dt]
                    
                    # Apply end date filter
                    if end_date:
                        inacbg_df = inacbg_df[inacbg_df['ADMISSION_DATE_DT'] <= end_dt]
                    
                    # Remove temporary datetime column
                    inacbg_df = inacbg_df.drop('ADMISSION_DATE_DT', axis=1)
                    
                    # Check if any data remains after filtering
                    if inacbg_df.empty:
                        return None, f"No data found for the specified date range: {start_date} to {end_date}"
                    
                except Exception as e:
                    return None, f"Error processing date filter: {str(e)}"
            
            # Convert numeric columns
            numeric_columns = ['LOS', 'TOTAL_TARIF', 'TARIF_RS']
            for col in numeric_columns:
                if col in inacbg_df.columns:
                    inacbg_df[col] = pd.to_numeric(inacbg_df[col], errors='coerce').fillna(0)
            
            # Group by INACBG and calculate aggregated statistics
            grouped = inacbg_df.groupby('INACBG').agg({
                'INACBG': 'count',  # Count of patients
                'LOS': ['min', 'mean', 'max'],  # Min, Average, Max LOS
                'TOTAL_TARIF': 'sum',  # Total claim
                'TARIF_RS': 'sum'  # Total billing RS
            }).round(2)
            
            # Flatten column names
            grouped.columns = ['JML_PASIEN', 'MIN_LOS', 'AV_LOS', 'MAX_LOS', 'TOTAL_CLAIM', 'TOTAL_BILLING_RS']
            
            # Calculate SELISIH (TOTAL_CLAIM - TOTAL_BILLING_RS)
            grouped['SELISIH'] = grouped['TOTAL_CLAIM'] - grouped['TOTAL_BILLING_RS']
            
            # Calculate ARPP (Average Revenue Per Patient) = TOTAL_CLAIM / JML_PASIEN
            grouped['ARPP'] = (grouped['TOTAL_CLAIM'] / grouped['JML_PASIEN']).round(0)
            
            # Add placeholder columns for future use (set to 0 for now)
            grouped['TOTAL_PENUNJANG'] = 0
            grouped['TOTAL_OBAT'] = 0
            grouped['TOTAL_BMHP_ALKES'] = 0
            grouped['TOTAL_SEWA_ALAT'] = 0
            
            # Reset index to make INACBG a column
            grouped = grouped.reset_index()
            
            # Reorder columns to match the required format
            final_columns = [
                'INACBG', 'JML_PASIEN', 'MIN_LOS', 'AV_LOS', 'MAX_LOS', 
                'TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH', 'ARPP',
                'TOTAL_PENUNJANG', 'TOTAL_OBAT', 'TOTAL_BMHP_ALKES', 'TOTAL_SEWA_ALAT'
            ]
            
            # Ensure all columns exist
            for col in final_columns:
                if col not in grouped.columns:
                    grouped[col] = 0
            
            grouped = grouped[final_columns]
            
            # Format financial columns to Indonesian Rupiah format
            financial_columns = ['TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH', 'ARPP', 'TOTAL_PENUNJANG', 'TOTAL_OBAT', 'TOTAL_BMHP_ALKES', 'TOTAL_SEWA_ALAT']
            for col in financial_columns:
                if col in grouped.columns:
                    grouped[col] = grouped[col].apply(format_rupiah)
            
            # Apply sorting if specified
            if sort_column and sort_column in grouped.columns:
                try:
                    # Handle numeric columns for proper sorting
                    if sort_column in ['JML_PASIEN', 'MIN_LOS', 'AV_LOS', 'MAX_LOS', 'TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH', 'ARPP', 'TOTAL_PENUNJANG', 'TOTAL_OBAT', 'TOTAL_BMHP_ALKES', 'TOTAL_SEWA_ALAT']:
                        # For financial columns that are now formatted as strings, we need to sort by the original numeric values
                        if sort_column in ['TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH', 'ARPP', 'TOTAL_PENUNJANG', 'TOTAL_OBAT', 'TOTAL_BMHP_ALKES', 'TOTAL_SEWA_ALAT']:
                            # Create temporary numeric columns for sorting
                            temp_col = f"{sort_column}_NUM"
                            grouped[temp_col] = grouped[sort_column].str.replace('Rp. ', '').str.replace('.', '').astype(float)
                            grouped = grouped.sort_values(by=temp_col, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                            grouped = grouped.drop(temp_col, axis=1)
                        else:
                            grouped = grouped.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                    else:
                        # For non-numeric columns, convert to string for sorting
                        grouped = grouped.sort_values(by=sort_column, ascending=(sort_order.upper() == 'ASC'), na_position='last')
                except Exception as e:
                    # Could not sort by column
                    pass
            
            return grouped, None
            
        except Exception as e:
            return None, f"Error processing INACBG data: {str(e)}"
    
    def get_inacbg_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get INACBG data as HTML table with sorting and date filtering"""
        inacbg_df, error = self.process_inacbg_data(sort_column, sort_order, start_date, end_date)
        
        if error:
            return "", error
        
        try:
            table_html = inacbg_df.to_html(classes='data-table', index=False)
            return table_html, None
        except Exception as e:
            return "", f"Error creating INACBG table: {str(e)}"
    
    def get_inacbg_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        """Get INACBG data as HTML table with specific column filtering, sorting, and date filtering"""
        try:
            # First get the base INACBG data
            inacbg_df, error = self.process_inacbg_data(sort_column, sort_order, start_date, end_date)
            
            if error:
                return "", error
            
            # Apply specific column filter
            if filter_column and filter_value and filter_column in inacbg_df.columns:
                try:
                    # Convert filter value to string for case-insensitive search
                    filter_value_str = str(filter_value).lower()
                    
                    # Apply filter (case-insensitive search)
                    if inacbg_df[filter_column].dtype == 'object':  # String columns
                        # Check if it's a formatted financial column
                        if filter_column in ['TOTAL_CLAIM', 'TOTAL_BILLING_RS', 'SELISIH', 'ARPP', 'TOTAL_PENUNJANG', 'TOTAL_OBAT', 'TOTAL_BMHP_ALKES', 'TOTAL_SEWA_ALAT']:
                            # For financial columns, try to match the formatted value or numeric value
                            try:
                                # Try to convert filter value to numeric and format it
                                numeric_value = float(filter_value)
                                formatted_value = format_rupiah(numeric_value)
                                inacbg_df = inacbg_df[inacbg_df[filter_column] == formatted_value]
                            except ValueError:
                                # If conversion fails, try string search
                                inacbg_df = inacbg_df[
                                    inacbg_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                                ]
                        else:
                            # Regular string search
                            inacbg_df = inacbg_df[
                                inacbg_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    else:  # Numeric columns
                        # Try to convert filter value to numeric for exact match
                        try:
                            numeric_value = float(filter_value)
                            inacbg_df = inacbg_df[inacbg_df[filter_column] == numeric_value]
                        except ValueError:
                            # If conversion fails, try string search
                            inacbg_df = inacbg_df[
                                inacbg_df[filter_column].astype(str).str.lower().str.contains(filter_value_str, na=False)
                            ]
                    
                    # Check if any data remains after filtering
                    if inacbg_df.empty:
                        return "<p>Tidak ada data yang ditemukan dengan filter yang diberikan.</p>", None
                        
                except Exception as e:
                    # Could not apply filter on column
                    pass
            
            # Create HTML table
            table_html = inacbg_df.to_html(classes='data-table', index=False)
            return table_html, None
            
        except Exception as e:
            return "", f"Error creating filtered INACBG table: {str(e)}"
    
    def get_inacbg_columns(self):
        """Get list of available columns for INACBG data sorting and filtering"""
        if self.data_handler.current_df is None:
            return []
        
        try:
            # Get the INACBG dataframe to see all available columns
            inacbg_df, error = self.process_inacbg_data()
            if error:
                return []
            
            return list(inacbg_df.columns)
        except Exception as e:
            return []
