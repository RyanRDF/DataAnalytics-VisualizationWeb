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
            'sep', 'mrn', 'nama_pasien', 'nokartu', 'dpjp',
            'admission_date', 'discharge_date', 'los', 'kelas_rawat',
            'inacbg', 'total_tarif', 'tarif_rs'
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
        numeric_columns = ['los', 'total_tarif', 'tarif_rs']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = safe_numeric_conversion(df[col])
        
        # Calculate additional financial metrics
        if 'total_tarif' in df.columns and 'tarif_rs' in df.columns:
            df['selisih_tarif'] = df['total_tarif'] - df['tarif_rs']
            df['persentase_selisih'] = (df['selisih_tarif'] / df['tarif_rs'] * 100).round(2)
        
        if 'total_tarif' in df.columns and 'los' in df.columns:
            df['tarif_per_hari'] = (df['total_tarif'] / df['los']).round(2)
        
        # Format currency columns
        currency_columns = ['total_tarif', 'tarif_rs', 'selisih_tarif', 'tarif_per_hari']
        for col in currency_columns:
            if col in df.columns:
                df[f'{col}_formatted'] = df[col].apply(format_rupiah)
        
        return df
