"""
LOS (Length of Stay) data handler
"""
import pandas as pd
from typing import List, Dict, Any

from core.base_handler import BaseHandler
from utils.formatters import format_rupiah
from utils.data_processing import safe_numeric_conversion


class LOSHandler(BaseHandler):
    """Handler for LOS analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for LOS analysis"""
        return [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE', 'TOTAL_TARIF', 'TARIF_RS'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "LOS"
    
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query LOS data from database with filters"""
        return self.db_query_service.get_los_data(filters)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process LOS data with required calculations"""
        # Convert numeric columns
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        
        # Calculate LOS metrics
        df['TARIF_PER_HARI'] = (df['TOTAL_TARIF'] / df['LOS']).round(2)
        df['TARIF_RS_PER_HARI'] = (df['TARIF_RS'] / df['LOS']).round(2)
        df['SELISIH_PER_HARI'] = df['TARIF_PER_HARI'] - df['TARIF_RS_PER_HARI']
        
        # Format currency columns
        df['TOTAL_TARIF_FORMATTED'] = df['TOTAL_TARIF'].apply(format_rupiah)
        df['TARIF_RS_FORMATTED'] = df['TARIF_RS'].apply(format_rupiah)
        df['TARIF_PER_HARI_FORMATTED'] = df['TARIF_PER_HARI'].apply(format_rupiah)
        df['TARIF_RS_PER_HARI_FORMATTED'] = df['TARIF_RS_PER_HARI'].apply(format_rupiah)
        df['SELISIH_PER_HARI_FORMATTED'] = df['SELISIH_PER_HARI'].apply(format_rupiah)
        
        # Reorder columns for better display
        column_order = [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE',
            'TOTAL_TARIF', 'TOTAL_TARIF_FORMATTED', 'TARIF_RS', 'TARIF_RS_FORMATTED',
            'TARIF_PER_HARI', 'TARIF_PER_HARI_FORMATTED',
            'TARIF_RS_PER_HARI', 'TARIF_RS_PER_HARI_FORMATTED',
            'SELISIH_PER_HARI', 'SELISIH_PER_HARI_FORMATTED'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
