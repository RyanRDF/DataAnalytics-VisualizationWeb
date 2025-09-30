"""
Selisih Tarif data handler
"""
import pandas as pd
from typing import List, Dict, Any

from core.base_handler import BaseHandler
from utils.formatters import format_rupiah
from utils.data_processing import safe_numeric_conversion, extract_diagnosis_codes


class SelisihTarifHandler(BaseHandler):
    """Handler for selisih tarif analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for selisih tarif analysis"""
        return [
            'SEP', 'MRN', 'LOS', 'DIAGLIST', 'PROCLIST', 'INACBG', 'DESKRIPSI_INACBG',
            'TOTAL_TARIF', 'TARIF_RS', 'ADMISSION_DATE', 'DISCHARGE_DATE'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "selisih tarif"
    
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query selisih tarif data from database with filters"""
        return self.db_query_service.get_selisih_tarif_data(filters)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process selisih tarif data with required calculations"""
        # Convert numeric columns
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        
        # Process DIAGLIST to extract PDX and SDX
        diagnosis_data = df['DIAGLIST'].apply(extract_diagnosis_codes)
        df['PDX'] = [item[0] for item in diagnosis_data]
        df['SDX'] = [item[1] for item in diagnosis_data]
        
        # Calculate selisih tarif metrics
        df['SELISIH_TARIF'] = df['TOTAL_TARIF'] - df['TARIF_RS']
        df['PERSENTASE_SELISIH'] = (df['SELISIH_TARIF'] / df['TARIF_RS'] * 100).round(2)
        
        # Format currency columns
        df['TOTAL_TARIF_FORMATTED'] = df['TOTAL_TARIF'].apply(format_rupiah)
        df['TARIF_RS_FORMATTED'] = df['TARIF_RS'].apply(format_rupiah)
        df['SELISIH_TARIF_FORMATTED'] = df['SELISIH_TARIF'].apply(format_rupiah)
        
        # Reorder columns for better display
        column_order = [
            'SEP', 'MRN', 'LOS', 'INACBG', 'DESKRIPSI_INACBG',
            'PDX', 'SDX', 'DIAGLIST', 'PROCLIST',
            'TOTAL_TARIF', 'TOTAL_TARIF_FORMATTED', 'TARIF_RS', 'TARIF_RS_FORMATTED',
            'SELISIH_TARIF', 'SELISIH_TARIF_FORMATTED', 'PERSENTASE_SELISIH',
            'ADMISSION_DATE', 'DISCHARGE_DATE'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
