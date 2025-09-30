"""
INACBG data handler
"""
import pandas as pd
from typing import List, Dict, Any

from core.base_handler import BaseHandler
from utils.formatters import format_rupiah
from utils.data_processing import safe_numeric_conversion


class INACBGHandler(BaseHandler):
    """Handler for INACBG analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for INACBG analysis"""
        return [
            'INACBG', 'DESKRIPSI_INACBG', 'TOTAL_TARIF', 'TARIF_RS',
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "INACBG"
    
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query INACBG data from database with filters"""
        return self.db_query_service.get_inacbg_data(filters)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process INACBG data with grouping and aggregation"""
        # Convert numeric columns
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        
        # Group by INACBG and calculate statistics
        grouped = df.groupby(['INACBG', 'DESKRIPSI_INACBG']).agg({
            'NAMA_PASIEN': 'count',
            'LOS': ['mean', 'min', 'max'],
            'TOTAL_TARIF': ['mean', 'sum'],
            'TARIF_RS': ['mean', 'sum']
        }).round(2)
        
        # Flatten column names
        grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
        grouped = grouped.reset_index()
        
        # Rename columns for better readability
        column_mapping = {
            'NAMA_PASIEN_count': 'JUMLAH_PASIEN',
            'LOS_mean': 'RATA_RATA_LOS',
            'LOS_min': 'MIN_LOS',
            'LOS_max': 'MAX_LOS',
            'TOTAL_TARIF_mean': 'RATA_RATA_TOTAL_TARIF',
            'TOTAL_TARIF_sum': 'TOTAL_TARIF_SUM',
            'TARIF_RS_mean': 'RATA_RATA_TARIF_RS',
            'TARIF_RS_sum': 'TARIF_RS_SUM'
        }
        
        grouped = grouped.rename(columns=column_mapping)
        
        # Calculate additional metrics
        grouped['SELISIH_TARIF'] = grouped['RATA_RATA_TOTAL_TARIF'] - grouped['RATA_RATA_TARIF_RS']
        grouped['PERSENTASE_SELISIH'] = (grouped['SELISIH_TARIF'] / grouped['RATA_RATA_TARIF_RS'] * 100).round(2)
        
        # Format currency columns
        currency_columns = ['RATA_RATA_TOTAL_TARIF', 'TOTAL_TARIF_SUM', 'RATA_RATA_TARIF_RS', 'TARIF_RS_SUM', 'SELISIH_TARIF']
        for col in currency_columns:
            if col in grouped.columns:
                grouped[f'{col}_FORMATTED'] = grouped[col].apply(format_rupiah)
        
        return grouped
