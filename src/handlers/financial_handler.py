"""
Financial data handler
"""
import pandas as pd
from typing import List

from ..core.base_handler import BaseHandler
from ..utils.formatters import format_rupiah
from ..utils.data_processing import safe_numeric_conversion


class FinancialHandler(BaseHandler):
    """Handler for financial data analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for financial analysis"""
        return [
            'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF', 
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN', 
            'NOKARTU', 'TOTAL_TARIF', 'TARIF_RS'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "financial"
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process financial data with required calculations"""
        # Convert LOS to numeric, handling any non-numeric values
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        
        # Convert TOTAL_TARIF and TARIF_RS to numeric
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        
        # Calculate additional financial metrics
        df['SELISIH_TARIF'] = df['TOTAL_TARIF'] - df['TARIF_RS']
        df['PERSENTASE_SELISIH'] = (df['SELISIH_TARIF'] / df['TARIF_RS'] * 100).round(2)
        df['TARIF_PER_HARI'] = (df['TOTAL_TARIF'] / df['LOS']).round(2)
        
        # Format currency columns
        df['TOTAL_TARIF_FORMATTED'] = df['TOTAL_TARIF'].apply(format_rupiah)
        df['TARIF_RS_FORMATTED'] = df['TARIF_RS'].apply(format_rupiah)
        df['SELISIH_TARIF_FORMATTED'] = df['SELISIH_TARIF'].apply(format_rupiah)
        df['TARIF_PER_HARI_FORMATTED'] = df['TARIF_PER_HARI'].apply(format_rupiah)
        
        # Reorder columns for better display
        column_order = [
            'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF',
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN', 'NOKARTU',
            'TOTAL_TARIF', 'TOTAL_TARIF_FORMATTED', 'TARIF_RS', 'TARIF_RS_FORMATTED',
            'SELISIH_TARIF', 'SELISIH_TARIF_FORMATTED', 'PERSENTASE_SELISIH',
            'TARIF_PER_HARI', 'TARIF_PER_HARI_FORMATTED'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
