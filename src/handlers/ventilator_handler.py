"""
Ventilator data handler
"""
import pandas as pd
import json
from typing import List, Dict, Any

from core.base_handler import BaseHandler
from utils.formatters import format_rupiah
from utils.data_processing import safe_numeric_conversion


class VentilatorHandler(BaseHandler):
    """Handler for ventilator analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for ventilator analysis"""
        return [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE', 'TOTAL_TARIF', 'TARIF_RS',
            'VENT_HOUR', 'ICU_INDIKATOR', 'ICU_LOS'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "ventilator"
    
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query ventilator data from database with filters"""
        return self.db_query_service.get_ventilator_data(filters)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process ventilator data with required calculations"""
        if df.empty:
            return df
            
        # Convert numeric columns
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        df['VENT_HOUR'] = safe_numeric_conversion(df['VENT_HOUR'])
        df['ICU_LOS'] = safe_numeric_conversion(df['ICU_LOS'])
        
        # Calculate ventilator metrics
        df['VENTILATOR_DAYS'] = (df['VENT_HOUR'] / 24).round(2)
        
        # Handle division by zero for ventilator cost calculations
        df['VENTILATOR_COST_PER_HOUR'] = df.apply(
            lambda row: (row['TOTAL_TARIF'] / row['VENT_HOUR']) if row['VENT_HOUR'] > 0 else 0, axis=1
        ).round(2)
        
        df['VENTILATOR_COST_PER_DAY'] = df.apply(
            lambda row: (row['TOTAL_TARIF'] / row['VENTILATOR_DAYS']) if row['VENTILATOR_DAYS'] > 0 else 0, axis=1
        ).round(2)
        
        df['VENTILATOR_PERCENTAGE_OF_TOTAL'] = df.apply(
            lambda row: (row['VENT_HOUR'] / row['LOS'] * 100) if row['LOS'] > 0 else 0, axis=1
        ).round(2)
        
        # Add ventilator status indicator
        df['VENTILATOR_STATUS'] = df['VENT_HOUR'].apply(
            lambda x: 'Menggunakan Ventilator' if x > 0 else 'Tidak Menggunakan Ventilator'
        )
        
        # Format currency columns
        currency_columns = ['TOTAL_TARIF', 'TARIF_RS', 'VENTILATOR_COST_PER_HOUR', 'VENTILATOR_COST_PER_DAY']
        for col in currency_columns:
            if col in df.columns:
                df[f'{col}_FORMATTED'] = df[col].apply(format_rupiah)
        
        # Remove duplicate numeric columns, keep only formatted versions
        columns_to_remove = ['TOTAL_TARIF', 'TARIF_RS', 'VENTILATOR_COST_PER_HOUR', 'VENTILATOR_COST_PER_DAY']
        for col in columns_to_remove:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        # Reorder columns for better display
        column_order = [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE',
            'VENT_HOUR', 'VENTILATOR_DAYS', 'VENTILATOR_STATUS', 'ICU_INDIKATOR', 'ICU_LOS',
            'TOTAL_TARIF_FORMATTED', 'TARIF_RS_FORMATTED',
            'VENTILATOR_COST_PER_HOUR_FORMATTED', 'VENTILATOR_COST_PER_DAY_FORMATTED',
            'VENTILATOR_PERCENTAGE_OF_TOTAL'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
