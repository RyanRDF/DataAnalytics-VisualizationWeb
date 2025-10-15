"""
Main data handler that coordinates all data processing
"""
import pandas as pd
import os
from typing import Optional, Tuple

from core.data_processor import DataProcessor
from handlers.financial_handler import FinancialHandler
from handlers.patient_handler import PatientHandler
from handlers.selisih_tarif_handler import SelisihTarifHandler
from handlers.los_handler import LOSHandler
from handlers.inacbg_handler import INACBGHandler
from handlers.ventilator_handler import VentilatorHandler


class DataHandler:
    """
    Main data handler that coordinates all data processing and analysis
    """
    
    def __init__(self):
        self.current_df = None
        self.data_processor = DataProcessor()
        self.accumulated_data = None  # Store accumulated data
        self.upload_count = 0  # Track number of uploads
        
        # Initialize specialized handlers
        self.financial_handler = FinancialHandler(self)
        self.patient_handler = PatientHandler(self)
        self.selisih_tarif_handler = SelisihTarifHandler(self)
        self.los_handler = LOSHandler(self)
        self.inacbg_handler = INACBGHandler(self)
        self.ventilator_handler = VentilatorHandler(self)
    
    def load_data_from_file(self, filepath: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Load data from uploaded file and process it, accumulating with existing data
        
        Args:
            filepath: Path to the uploaded file
            
        Returns:
            Tuple of (processed_dataframe, error_message)
        """
        try:
            # Read the uploaded file based on extension
            if filepath.lower().endswith('.xlsx') or filepath.lower().endswith('.xls'):
                # Enhanced Excel reading with better error handling
                try:
                    new_df = pd.read_excel(filepath, header=0, na_values=['', ' ', '-', 'N/A', 'NULL'])
                except Exception as e:
                    # Try alternative reading methods
                    try:
                        new_df = pd.read_excel(filepath, header=0, engine='openpyxl')
                    except Exception as e2:
                        try:
                            new_df = pd.read_excel(filepath, header=0, engine='xlrd')
                        except Exception as e3:
                            raise Exception(f"Failed to read Excel file: {str(e)}. Alternative methods also failed: {str(e2)}, {str(e3)}")
            else:
                new_df = pd.read_csv(filepath, sep='\t')
            
            # Log file reading results for debugging
            print(f"📊 DataHandler - File read successfully:")
            print(f"  - File: {filepath}")
            print(f"  - Rows: {len(new_df)}")
            print(f"  - Columns: {len(new_df.columns)}")
            print(f"  - Column names: {list(new_df.columns)}")
            
            # If this is the first upload, initialize accumulated data
            if self.accumulated_data is None:
                self.accumulated_data = new_df.copy()
                self.upload_count = 1
            else:
                # Append new data to accumulated data
                self.accumulated_data = pd.concat([self.accumulated_data, new_df], ignore_index=True)
                self.upload_count += 1
            
            # Load accumulated data into processor and process it
            self.data_processor.load_raw_data(self.accumulated_data)
            processed_df = self.data_processor.process_data()
            
            # Update current_df to use processed data
            self.current_df = processed_df
            
            return processed_df, None
        except Exception as e:
            return None, f"Error loading and processing file: {str(e)}"
    
    def get_raw_data_table(self) -> Tuple[str, bool]:
        """
        Get processed data as HTML table
        
        Returns:
            Tuple of (html_table, has_data)
        """
        if self.current_df is None:
            return "", False
        
        try:
            table_html = self.current_df.to_html(classes='data-table', index=False)
            return table_html, True
        except Exception as e:
            return "", False
    
    def get_processed_data(self) -> Optional[pd.DataFrame]:
        """Get processed data"""
        if self.data_processor.has_processed_data():
            return self.data_processor.get_processed_data()
        return None
    
    def get_raw_data(self) -> Optional[pd.DataFrame]:
        """Get raw data before processing"""
        if self.data_processor.has_data():
            return self.data_processor.get_raw_data()
        return None
    
    def get_processing_summary(self) -> dict:
        """Get summary of data processing"""
        if self.data_processor.has_processed_data():
            summary = self.data_processor.get_processing_summary()
            # Add accumulation info
            summary['upload_count'] = self.upload_count
            summary['total_files'] = self.upload_count
            if self.accumulated_data is not None:
                summary['accumulated_rows'] = len(self.accumulated_data)
            return summary
        return {"error": "No processed data available"}
    
    def has_data(self) -> bool:
        """Check if data is loaded"""
        # Check if data exists in database
        try:
            from core.database import DataAnalytics
            count = DataAnalytics.query.count()
            return count > 0
        except Exception:
            # Fallback to checking current_df
            return self.current_df is not None
    
    def validate_file(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate uploaded file
        
        Args:
            filename: Name of the uploaded file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        allowed_extensions = ['.txt', '.xlsx', '.xls']
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            return False, "Please upload a .txt, .xlsx, or .xls file"
        return True, None
    
    def save_uploaded_file(self, file, upload_folder: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Save uploaded file to temporary location
        
        Args:
            file: Uploaded file object
            upload_folder: Path to upload folder
            
        Returns:
            Tuple of (filepath, error_message)
        """
        try:
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            return filepath, None
        except Exception as e:
            return None, f"Error saving file: {str(e)}"
    
    def cleanup_file(self, filepath: str):
        """
        Clean up uploaded file
        
        Args:
            filepath: Path to file to clean up
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            # Could not remove file
            pass
    
    def clear_all_data(self):
        """
        Clear all accumulated data and reset to initial state
        """
        self.current_df = None
        self.accumulated_data = None
        self.upload_count = 0
        self.data_processor = DataProcessor()  # Reset processor
    
    def get_accumulation_info(self) -> dict:
        """
        Get information about data accumulation
        
        Returns:
            Dictionary with accumulation information
        """
        return {
            'upload_count': self.upload_count,
            'has_data': self.has_data(),
            'accumulated_rows': len(self.accumulated_data) if self.accumulated_data is not None else 0,
            'processed_rows': len(self.current_df) if self.current_df is not None else 0
        }
