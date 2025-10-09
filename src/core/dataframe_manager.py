"""
DataFrame Manager untuk mengelola DataFrame pandas
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class DataFrameManager:
    """Class untuk mengelola DataFrame pandas"""
    
    def __init__(self):
        self.current_dataframe: Optional[pd.DataFrame] = None
        self.original_dataframe: Optional[pd.DataFrame] = None
        self.valid_data: Optional[pd.DataFrame] = None
        self.duplicate_data: Optional[pd.DataFrame] = None
        
    def set_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Set DataFrame yang akan diproses
        
        Args:
            df: DataFrame yang akan diset
            
        Returns:
            Dict dengan informasi DataFrame
        """
        try:
            self.current_dataframe = df.copy()
            self.original_dataframe = df.copy()
            
            info = {
                'success': True,
                'total_rows': len(df),
                'total_columns': len(df.columns),
                'columns': list(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum(),
                'error': None
            }
            
            logger.info(f"DataFrame set: {info['total_rows']} rows, {info['total_columns']} columns")
            return info
            
        except Exception as e:
            logger.error(f"Error setting DataFrame: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_rows': 0,
                'total_columns': 0
            }
    
    def get_dataframe_info(self) -> Dict[str, Any]:
        """Get informasi DataFrame saat ini"""
        if self.current_dataframe is None:
            return {
                'has_data': False,
                'total_rows': 0,
                'total_columns': 0
            }
        
        return {
            'has_data': True,
            'total_rows': len(self.current_dataframe),
            'total_columns': len(self.current_dataframe.columns),
            'columns': list(self.current_dataframe.columns),
            'memory_usage': self.current_dataframe.memory_usage(deep=True).sum()
        }
    
    def validate_dataframe(self) -> Dict[str, Any]:
        """
        Validasi DataFrame untuk memastikan data siap diproses
        
        Returns:
            Dict dengan hasil validasi
        """
        if self.current_dataframe is None:
            return {
                'is_valid': False,
                'error': 'DataFrame tidak ada'
            }
        
        try:
            validation_result = {
                'is_valid': True,
                'total_rows': len(self.current_dataframe),
                'empty_rows': 0,
                'missing_sep': 0,
                'invalid_data': 0,
                'errors': []
            }
            
            # Check for empty rows
            empty_rows = self.current_dataframe.isnull().all(axis=1).sum()
            validation_result['empty_rows'] = empty_rows
            
            # Check for missing SEP (required for duplicate checking)
            if 'SEP' in self.current_dataframe.columns:
                missing_sep = self.current_dataframe['SEP'].isnull().sum()
                validation_result['missing_sep'] = missing_sep
                
                if missing_sep > 0:
                    validation_result['errors'].append(f'{missing_sep} rows missing SEP')
            else:
                validation_result['is_valid'] = False
                validation_result['errors'].append('Column SEP tidak ditemukan')
            
            # Check for completely empty DataFrame
            if len(self.current_dataframe) == 0:
                validation_result['is_valid'] = False
                validation_result['errors'].append('DataFrame kosong')
            
            # Check for all null rows
            if empty_rows == len(self.current_dataframe):
                validation_result['is_valid'] = False
                validation_result['errors'].append('Semua rows kosong')
            
            if validation_result['errors']:
                validation_result['is_valid'] = False
            
            logger.info(f"DataFrame validation: {validation_result}")
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating DataFrame: {e}")
            return {
                'is_valid': False,
                'error': str(e)
            }
    
    def separate_valid_duplicate_data(self, existing_seps: List[str]) -> Dict[str, Any]:
        """
        Pisahkan data valid dan duplikat berdasarkan SEP
        
        Args:
            existing_seps: List SEP yang sudah ada di database
            
        Returns:
            Dict dengan hasil pemisahan
        """
        if self.current_dataframe is None:
            return {
                'success': False,
                'error': 'DataFrame tidak ada'
            }
        
        try:
            # Convert existing_seps to set for faster lookup
            existing_seps_set = set(existing_seps)
            
            # Separate data based on SEP
            if 'SEP' in self.current_dataframe.columns:
                # Valid data: SEP not in existing_seps and not null
                valid_mask = (
                    self.current_dataframe['SEP'].notna() & 
                    (~self.current_dataframe['SEP'].isin(existing_seps_set))
                )
                
                # Duplicate data: SEP in existing_seps or null
                duplicate_mask = (
                    self.current_dataframe['SEP'].isna() | 
                    (self.current_dataframe['SEP'].isin(existing_seps_set))
                )
                
                self.valid_data = self.current_dataframe[valid_mask].copy()
                self.duplicate_data = self.current_dataframe[duplicate_mask].copy()
                
                result = {
                    'success': True,
                    'total_rows': len(self.current_dataframe),
                    'valid_rows': len(self.valid_data),
                    'duplicate_rows': len(self.duplicate_data),
                    'valid_data': self.valid_data,
                    'duplicate_data': self.duplicate_data
                }
                
                logger.info(f"Data separated: {result['valid_rows']} valid, {result['duplicate_rows']} duplicates")
                return result
            else:
                return {
                    'success': False,
                    'error': 'Column SEP tidak ditemukan'
                }
                
        except Exception as e:
            logger.error(f"Error separating data: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_valid_data(self) -> Optional[pd.DataFrame]:
        """Get data yang valid untuk diupload"""
        return self.valid_data
    
    def get_duplicate_data(self) -> Optional[pd.DataFrame]:
        """Get data yang duplikat"""
        return self.duplicate_data
    
    def clear_dataframe(self) -> Dict[str, Any]:
        """
        Clear semua DataFrame untuk persiapan upload berikutnya
        
        Returns:
            Dict dengan hasil clearing
        """
        try:
            self.current_dataframe = None
            self.original_dataframe = None
            self.valid_data = None
            self.duplicate_data = None
            
            logger.info("DataFrame cleared successfully")
            return {
                'success': True,
                'message': 'DataFrame berhasil dibersihkan'
            }
            
        except Exception as e:
            logger.error(f"Error clearing DataFrame: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_upload_summary(self) -> Dict[str, Any]:
        """Get summary untuk upload"""
        if self.valid_data is None and self.duplicate_data is None:
            return {
                'total_rows': 0,
                'valid_rows': 0,
                'duplicate_rows': 0,
                'rows_success': 0,
                'rows_failed': 0
            }
        
        valid_count = len(self.valid_data) if self.valid_data is not None else 0
        duplicate_count = len(self.duplicate_data) if self.duplicate_data is not None else 0
        
        return {
            'total_rows': valid_count + duplicate_count,
            'valid_rows': valid_count,
            'duplicate_rows': duplicate_count,
            'rows_success': valid_count,
            'rows_failed': duplicate_count
        }

