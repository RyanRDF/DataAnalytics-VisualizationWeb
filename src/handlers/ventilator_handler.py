"""
Ventilator data handler
"""
import pandas as pd
import json
from typing import List

from ..core.base_handler import BaseHandler
from ..utils.formatters import format_rupiah
from ..utils.data_processing import safe_numeric_conversion


class VentilatorHandler(BaseHandler):
    """Handler for ventilator analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for ventilator analysis"""
        return [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE', 'TOTAL_TARIF', 'TARIF_RS',
            'VENTILATOR_HOURS', 'VENTILATOR_COST'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "ventilator"
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process ventilator data with required calculations"""
        # Convert numeric columns
        df['LOS'] = safe_numeric_conversion(df['LOS'])
        df['TOTAL_TARIF'] = safe_numeric_conversion(df['TOTAL_TARIF'])
        df['TARIF_RS'] = safe_numeric_conversion(df['TARIF_RS'])
        df['VENTILATOR_HOURS'] = safe_numeric_conversion(df['VENTILATOR_HOURS'])
        df['VENTILATOR_COST'] = safe_numeric_conversion(df['VENTILATOR_COST'])
        
        # Calculate ventilator metrics
        df['VENTILATOR_DAYS'] = (df['VENTILATOR_HOURS'] / 24).round(2)
        df['VENTILATOR_COST_PER_HOUR'] = (df['VENTILATOR_COST'] / df['VENTILATOR_HOURS']).round(2)
        df['VENTILATOR_COST_PER_DAY'] = (df['VENTILATOR_COST'] / df['VENTILATOR_DAYS']).round(2)
        df['VENTILATOR_PERCENTAGE_OF_TOTAL'] = (df['VENTILATOR_COST'] / df['TOTAL_TARIF'] * 100).round(2)
        
        # Format currency columns
        currency_columns = ['TOTAL_TARIF', 'TARIF_RS', 'VENTILATOR_COST', 'VENTILATOR_COST_PER_HOUR', 'VENTILATOR_COST_PER_DAY']
        for col in currency_columns:
            if col in df.columns:
                df[f'{col}_FORMATTED'] = df[col].apply(format_rupiah)
        
        # Reorder columns for better display
        column_order = [
            'SEP', 'MRN', 'NAMA_PASIEN', 'INACBG', 'DESKRIPSI_INACBG',
            'LOS', 'ADMISSION_DATE', 'DISCHARGE_DATE',
            'VENTILATOR_HOURS', 'VENTILATOR_DAYS',
            'TOTAL_TARIF', 'TOTAL_TARIF_FORMATTED', 'TARIF_RS', 'TARIF_RS_FORMATTED',
            'VENTILATOR_COST', 'VENTILATOR_COST_FORMATTED',
            'VENTILATOR_COST_PER_HOUR', 'VENTILATOR_COST_PER_HOUR_FORMATTED',
            'VENTILATOR_COST_PER_DAY', 'VENTILATOR_COST_PER_DAY_FORMATTED',
            'VENTILATOR_PERCENTAGE_OF_TOTAL'
        ]
        
        # Only include columns that exist in the dataframe
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
