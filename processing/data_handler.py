import pandas as pd
import numpy as np
import os
from .data_processor import DataProcessor
from .financial_handler import FinancialHandler
from .patient_handler import PatientHandler
from .selisih_tarif_handler import SelisihTarifHandler
from .los_handler import LOSHandler
from .inacbg_handler import INACBGHandler
from .ventilator_handler import VentilatorHandler

class DataHandler:
    def __init__(self):
        self.current_df = None
        self.data_processor = DataProcessor()
        # Initialize specialized handlers
        self.financial_handler = FinancialHandler(self)
        self.patient_handler = PatientHandler(self)
        self.selisih_tarif_handler = SelisihTarifHandler(self)
        self.los_handler = LOSHandler(self)
        self.inacbg_handler = INACBGHandler(self)
        self.ventilator_handler = VentilatorHandler(self)
    
    def load_data_from_file(self, filepath):
        """Load data from uploaded file and process it"""
        try:
            # Read the uploaded file with tab separator
            df = pd.read_csv(filepath, sep='\t')
            self.current_df = df
            
            # Load raw data into processor and process it
            self.data_processor.load_raw_data(df)
            processed_df = self.data_processor.process_data()
            
            # Update current_df to use processed data
            self.current_df = processed_df
            
            return processed_df, None
        except Exception as e:
            return None, f"Error loading and processing file: {str(e)}"
    
    def get_raw_data_table(self):
        """Get processed data as HTML table (shows processed data, not raw)"""
        if self.current_df is None:
            return "", False
        
        try:
            table_html = self.current_df.to_html(classes='data-table', index=False)
            return table_html, True
        except Exception as e:
            return "", False
    
    def get_processed_data(self):
        """Get processed data"""
        if self.data_processor.has_processed_data():
            return self.data_processor.get_processed_data()
        return None
    
    def get_raw_data(self):
        """Get raw data before processing"""
        if self.data_processor.has_data():
            return self.data_processor.get_raw_data()
        return None
    
    def get_processing_summary(self):
        """Get summary of data processing"""
        if self.data_processor.has_processed_data():
            return self.data_processor.get_processing_summary()
        return {"error": "No processed data available"}
    
    # Patient data methods - delegate to patient handler
    def process_patient_data(self):
        return self.patient_handler.process_patient_data()
    
    def get_patient_table(self):
        return self.patient_handler.get_patient_table()
    
    def process_patient_data_with_filters(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.patient_handler.process_patient_data_with_filters(sort_column, sort_order, start_date, end_date)
    
    def get_patient_table_with_filters(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.patient_handler.get_patient_table_with_filters(sort_column, sort_order, start_date, end_date)
    
    def get_patient_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.patient_handler.get_patient_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_patient_columns(self):
        return self.patient_handler.get_patient_columns()
    
    # Financial data methods - delegate to financial handler
    def process_financial_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.financial_handler.process_financial_data(sort_column, sort_order, start_date, end_date)
    
    def get_financial_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.financial_handler.get_financial_table(sort_column, sort_order, start_date, end_date)
    
    def get_financial_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.financial_handler.get_financial_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_financial_columns(self):
        return self.financial_handler.get_financial_columns()
    
    # Selisih tarif data methods - delegate to selisih tarif handler
    def process_selisih_tarif_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.selisih_tarif_handler.process_selisih_tarif_data(sort_column, sort_order, start_date, end_date)
    
    def get_selisih_tarif_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.selisih_tarif_handler.get_selisih_tarif_table(sort_column, sort_order, start_date, end_date)
    
    def get_selisih_tarif_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.selisih_tarif_handler.get_selisih_tarif_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_selisih_tarif_columns(self):
        return self.selisih_tarif_handler.get_selisih_tarif_columns()
    
    # LOS data methods - delegate to los handler
    def process_los_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.los_handler.process_los_data(sort_column, sort_order, start_date, end_date)
    
    def get_los_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.los_handler.get_los_table(sort_column, sort_order, start_date, end_date)
    
    def get_los_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.los_handler.get_los_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_los_columns(self):
        return self.los_handler.get_los_columns()
    
    # INACBG data methods - delegate to inacbg handler
    def process_inacbg_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.inacbg_handler.process_inacbg_data(sort_column, sort_order, start_date, end_date)
    
    def get_inacbg_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.inacbg_handler.get_inacbg_table(sort_column, sort_order, start_date, end_date)
    
    def get_inacbg_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.inacbg_handler.get_inacbg_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_inacbg_columns(self):
        return self.inacbg_handler.get_inacbg_columns()
    
    # Ventilator data methods - delegate to ventilator handler
    def process_ventilator_data(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.ventilator_handler.process_ventilator_data(sort_column, sort_order, start_date, end_date)
    
    def get_ventilator_table(self, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.ventilator_handler.get_ventilator_table(sort_column, sort_order, start_date, end_date)
    
    def get_ventilator_table_with_specific_filter(self, filter_column, filter_value, sort_column=None, sort_order='ASC', start_date=None, end_date=None):
        return self.ventilator_handler.get_ventilator_table_with_specific_filter(filter_column, filter_value, sort_column, sort_order, start_date, end_date)
    
    def get_ventilator_columns(self):
        return self.ventilator_handler.get_ventilator_columns()
    
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
