"""
Duplicate Checker untuk memverifikasi duplikasi data berdasarkan SEP
"""
import pandas as pd
from typing import Dict, Any, List, Set
import logging
from core.database import db, DataAnalytics

logger = logging.getLogger(__name__)

class DuplicateChecker:
    """Class untuk mengecek duplikasi data berdasarkan SEP"""
    
    def __init__(self):
        pass
    
    def get_existing_seps(self) -> Set[str]:
        """
        Ambil semua SEP yang sudah ada di database
        
        Returns:
            Set SEP yang sudah ada
        """
        try:
            # Query semua SEP dari database
            existing_seps = db.session.query(DataAnalytics.sep).filter(
                DataAnalytics.sep.isnot(None)
            ).all()
            
            # Convert ke set untuk lookup yang lebih cepat
            sep_set = {sep[0] for sep in existing_seps if sep[0] is not None}
            
            logger.info(f"Found {len(sep_set)} existing SEPs in database")
            return sep_set
            
        except Exception as e:
            logger.error(f"Error getting existing SEPs: {e}")
            return set()
    
    def check_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Cek duplikasi dalam DataFrame berdasarkan SEP
        
        Args:
            df: DataFrame yang akan dicek
            
        Returns:
            Dict dengan hasil pengecekan duplikasi
        """
        try:
            if df is None or df.empty:
                return {
                    'success': False,
                    'error': 'DataFrame kosong',
                    'total_rows': 0,
                    'new_rows': 0,
                    'duplicate_rows': 0,
                    'duplicate_seps': []
                }
            
            # Get existing SEPs from database
            existing_seps = self.get_existing_seps()
            
            # Check if SEP column exists
            if 'SEP' not in df.columns:
                return {
                    'success': False,
                    'error': 'Column SEP tidak ditemukan',
                    'total_rows': len(df),
                    'new_rows': 0,
                    'duplicate_rows': 0,
                    'duplicate_seps': []
                }
            
            # Separate new and duplicate data
            new_mask = (
                df['SEP'].notna() & 
                (~df['SEP'].isin(existing_seps))
            )
            
            duplicate_mask = (
                df['SEP'].isna() | 
                (df['SEP'].isin(existing_seps))
            )
            
            new_data = df[new_mask]
            duplicate_data = df[duplicate_mask]
            
            # Get list of duplicate SEPs
            duplicate_seps = []
            if not duplicate_data.empty and 'SEP' in duplicate_data.columns:
                duplicate_seps = duplicate_data['SEP'].dropna().unique().tolist()
            
            result = {
                'success': True,
                'total_rows': len(df),
                'new_rows': len(new_data),
                'duplicate_rows': len(duplicate_data),
                'duplicate_seps': duplicate_seps,
                'new_data': new_data,
                'duplicate_data': duplicate_data
            }
            
            logger.info(f"Duplicate check completed: {result['new_rows']} new, {result['duplicate_rows']} duplicates")
            return result
            
        except Exception as e:
            logger.error(f"Error checking duplicates: {e}")
            return {
                'success': False,
                'error': str(e),
                'total_rows': len(df) if df is not None else 0,
                'new_rows': 0,
                'duplicate_rows': 0,
                'duplicate_seps': []
            }
    
    def get_duplicate_details(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get detail informasi duplikasi
        
        Args:
            df: DataFrame yang akan dianalisa
            
        Returns:
            Dict dengan detail duplikasi
        """
        try:
            if df is None or df.empty or 'SEP' not in df.columns:
                return {
                    'success': False,
                    'error': 'DataFrame kosong atau tidak memiliki column SEP'
                }
            
            # Check for internal duplicates within the file
            internal_duplicates = df[df.duplicated(subset=['SEP'], keep=False)]
            
            # Check for database duplicates
            existing_seps = self.get_existing_seps()
            db_duplicates = df[df['SEP'].isin(existing_seps)]
            
            # Check for null SEPs
            null_seps = df[df['SEP'].isna()]
            
            result = {
                'success': True,
                'total_rows': len(df),
                'internal_duplicates': len(internal_duplicates),
                'database_duplicates': len(db_duplicates),
                'null_seps': len(null_seps),
                'unique_seps': df['SEP'].nunique(),
                'internal_duplicate_seps': internal_duplicates['SEP'].unique().tolist() if not internal_duplicates.empty else [],
                'database_duplicate_seps': db_duplicates['SEP'].unique().tolist() if not db_duplicates.empty else []
            }
            
            logger.info(f"Duplicate details: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting duplicate details: {e}")
            return {
                'success': False,
                'error': str(e)
            }
