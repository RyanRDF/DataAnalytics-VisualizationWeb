"""
Financial data handler
"""
import pandas as pd
from typing import List, Dict, Any

from core.base_handler import BaseHandler
from utils.formatters import format_rupiah
from utils.data_processing import safe_numeric_conversion


class FinancialHandler(BaseHandler):
    """Handler for financial data analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for financial analysis"""
        return [
            'SEP', 'MRN', 'NAMA_PASIEN', 'NOKARTU', 'DPJP',
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'KELAS_RAWAT',
            'INACBG', 'TOTAL_TARIF', 'TARIF_RS', 'PROSEDUR_NON_BEDAH',
            'PROSEDUR_BEDAH', 'KONSULTASI', 'TENAGA_AHLI', 'KEPERAWATAN',
            'PENUNJANG', 'RADIOLOGI', 'LABORATORIUM', 'PELAYANAN_DARAH',
            'KAMAR_AKOMODASI', 'OBAT'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "financial"
    
    def _query_database(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """Query financial data from database"""
        return self.db_query_service.get_financial_data(filters)
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process financial data with required calculations"""
        if df.empty:
            return df
        
        # Convert numeric columns
        numeric_columns = ['LOS', 'TOTAL_TARIF', 'TARIF_RS']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = safe_numeric_conversion(df[col])
        
        # Calculate additional financial metrics
        if 'TOTAL_TARIF' in df.columns and 'TARIF_RS' in df.columns:
            df['SELISIH_TARIF'] = df['TOTAL_TARIF'] - df['TARIF_RS']
            df['PERSENTASE_SELISIH'] = (df['SELISIH_TARIF'] / df['TARIF_RS'] * 100).round(2)
        
        if 'TOTAL_TARIF' in df.columns and 'LOS' in df.columns:
            df['TARIF_PER_HARI'] = (df['TOTAL_TARIF'] / df['LOS']).round(2)
        
        # Format currency columns
        currency_columns = ['TOTAL_TARIF', 'TARIF_RS', 'SELISIH_TARIF', 'TARIF_PER_HARI']
        for col in currency_columns:
            if col in df.columns:
                df[f'{col}_FORMATTED'] = df[col].apply(format_rupiah)
        
        # Remove duplicate numeric columns, keep only formatted versions
        columns_to_remove = ['TOTAL_TARIF', 'TARIF_RS', 'SELISIH_TARIF', 'TARIF_PER_HARI']
        for col in columns_to_remove:
            if col in df.columns:
                df = df.drop(columns=[col])
        
        return df
