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
        if df.empty:
            return df
        
        # Data sudah di-group dari database, kita hanya perlu memproses dan memformat
        # Convert numeric columns
        numeric_columns = ['rata_los', 'min_los', 'max_los', 'rata_tarif', 'total_tarif', 'rata_tarif_rs', 'total_tarif_rs']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = safe_numeric_conversion(df[col])
        
        # Rename columns for better readability
        column_mapping = {
            'jumlah_kunjungan': 'jumlah_pasien',
            'rata_los': 'rata_rata_los',
            'rata_tarif': 'rata_rata_total_tarif',
            'rata_tarif_rs': 'rata_rata_tarif_rs'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Calculate additional metrics
        if 'rata_rata_total_tarif' in df.columns and 'rata_rata_tarif_rs' in df.columns:
            df['selisih_tarif'] = df['rata_rata_total_tarif'] - df['rata_rata_tarif_rs']
            df['persentase_selisih'] = (df['selisih_tarif'] / df['rata_rata_tarif_rs'] * 100).round(2)
        
        # Format currency columns
        currency_columns = ['rata_rata_total_tarif', 'total_tarif', 'rata_rata_tarif_rs', 'total_tarif_rs', 'selisih_tarif']
        for col in currency_columns:
            if col in df.columns:
                df[f'{col}_formatted'] = df[col].apply(format_rupiah)
        
        # Remove duplicate numeric columns, keep only formatted versions
        for col in currency_columns:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        # Reorder columns for better display
        column_order = [
            'INACBG', 'DESKRIPSI_INACBG', 'jumlah_pasien',
            'rata_rata_los', 'min_los', 'max_los',
            'rata_rata_total_tarif_formatted', 'total_tarif_formatted',
            'rata_rata_tarif_rs_formatted', 'total_tarif_rs_formatted',
            'selisih_tarif_formatted', 'persentase_selisih'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
