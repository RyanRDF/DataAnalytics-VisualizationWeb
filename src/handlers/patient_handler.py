"""
Patient data handler
"""
import pandas as pd
from typing import List

from ..core.base_handler import BaseHandler
from ..utils.data_processing import safe_numeric_conversion, calculate_age_in_days


class PatientHandler(BaseHandler):
    """Handler for patient data analysis"""
    
    def _get_required_columns(self) -> List[str]:
        """Get list of required columns for patient analysis"""
        return [
            'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF',
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'LOS', 'NAMA_PASIEN',
            'NOKARTU', 'BIRTH_DATE', 'BIRTH_WEIGHT', 'SEX',
            'DISCHARGE_STATUS', 'DIAGLIST', 'PROCLIST', 'ADL1', 'ADL2',
            'IN_SP', 'IN_SR', 'IN_SI', 'IN_SD', 'INACBG', 'SUBACUTE',
            'CHRONIC', 'SP', 'SR', 'SI', 'SD', 'DESKRIPSI_INACBG',
            'MRN', 'UMUR_TAHUN', 'UMUR_HARI', 'DPJP', 'SEP', 'PAYOR_ID',
            'CODER_ID', 'VERSI_INACBG', 'VERSI_GROUPER'
        ]
    
    def _get_view_name(self) -> str:
        """Get the view name for this handler"""
        return "patient"
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process patient data with all required columns"""
        # Check which columns exist in the data
        existing_columns = [col for col in self.required_columns if col in df.columns]
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        
        # Create a copy of the dataframe with existing patient columns
        patient_df = df[existing_columns].copy()
        
        # Fill missing columns with empty values
        for col in missing_columns:
            patient_df[col] = ''
        
        # Reorder columns to match the expected format
        final_columns = self.required_columns
        patient_df = patient_df.reindex(columns=final_columns)
        
        # Clean up data - replace None values with empty strings
        patient_df = patient_df.fillna('')
        
        # Convert numeric columns
        numeric_columns = ['LOS', 'BIRTH_WEIGHT', 'UMUR_TAHUN', 'UMUR_HARI']
        for col in numeric_columns:
            if col in patient_df.columns:
                patient_df[col] = safe_numeric_conversion(patient_df[col])
        
        # Calculate age in days if birth date and admission date are available
        if 'BIRTH_DATE' in patient_df.columns and 'ADMISSION_DATE' in patient_df.columns:
            patient_df['CALCULATED_AGE_DAYS'] = patient_df.apply(
                lambda row: calculate_age_in_days(row['BIRTH_DATE'], row['ADMISSION_DATE']), 
                axis=1
            )
        
        return patient_df
