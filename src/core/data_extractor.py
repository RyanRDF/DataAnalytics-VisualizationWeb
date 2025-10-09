"""
Data Extractor untuk mengekstrak data dari file txt dan xlsx ke DataFrame
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
import logging
import os

logger = logging.getLogger(__name__)

class DataExtractor:
    """Class untuk mengekstrak data dari file ke DataFrame"""
    
    def __init__(self):
        self.required_columns = [
            'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF', 'PTD', 'ADMISSION_DATE', 
            'DISCHARGE_DATE', 'BIRTH_DATE', 'BIRTH_WEIGHT', 'SEX', 'DISCHARGE_STATUS', 
            'DIAGLIST', 'PROCLIST', 'ADL1', 'ADL2', 'IN_SP', 'IN_SR', 'IN_SI', 'IN_SD', 
            'INACBG', 'SUBACUTE', 'CHRONIC', 'SP', 'SR', 'SI', 'SD', 'DESKRIPSI_INACBG', 
            'TARIF_INACBG', 'TARIF_SUBACUTE', 'TARIF_CHRONIC', 'DESKRIPSI_SP', 'TARIF_SP', 
            'DESKRIPSI_SR', 'TARIF_SR', 'DESKRIPSI_SI', 'TARIF_SI', 'DESKRIPSI_SD', 'TARIF_SD', 
            'TOTAL_TARIF', 'TARIF_RS', 'TARIF_POLI_EKS', 'LOS', 'ICU_INDIKATOR', 'ICU_LOS', 
            'VENT_HOUR', 'NAMA_PASIEN', 'MRN', 'UMUR_TAHUN', 'UMUR_HARI', 'DPJP', 'SEP', 
            'NOKARTU', 'PAYOR_ID', 'CODER_ID', 'VERSI_INACBG', 'VERSI_GROUPER', 'C1', 'C2', 
            'C3', 'C4', 'PROSEDUR_NON_BEDAH', 'PROSEDUR_BEDAH', 'KONSULTASI', 'TENAGA_AHLI', 
            'KEPERAWATAN', 'PENUNJANG', 'RADIOLOGI', 'LABORATORIUM', 'PELAYANAN_DARAH', 
            'REHABILITASI', 'KAMAR_AKOMODASI', 'RAWAT_INTENSIF', 'OBAT', 'ALKES', 'BMHP', 
            'SEWA_ALAT', 'OBAT_KRONIS', 'OBAT_KEMO'
        ]
    
    def extract_data(self, file_path: str, file_info: Dict[str, Any]) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """
        Ekstrak data dari file ke DataFrame
        
        Args:
            file_path: Path ke file
            file_info: Informasi file dari FileAnalyzer
            
        Returns:
            Tuple (DataFrame, extraction_info)
        """
        try:
            extraction_info = {
                'success': False,
                'rows_extracted': 0,
                'columns_found': 0,
                'missing_columns': [],
                'error': None
            }
            
            if file_info['file_type'] == 'excel':
                df, info = self._extract_excel(file_path, file_info)
            elif file_info['file_type'] == 'text':
                df, info = self._extract_text(file_path, file_info)
            else:
                raise ValueError(f"Tipe file tidak didukung: {file_info['file_type']}")
            
            extraction_info.update(info)
            
            if df is not None and not df.empty:
                extraction_info['success'] = True
                extraction_info['rows_extracted'] = len(df)
                extraction_info['columns_found'] = len(df.columns)
                
                # Check missing columns
                missing_cols = set(self.required_columns) - set(df.columns)
                extraction_info['missing_columns'] = list(missing_cols)
                
                logger.info(f"Data extracted successfully: {len(df)} rows, {len(df.columns)} columns")
            else:
                extraction_info['error'] = 'DataFrame kosong atau tidak dapat diekstrak'
            
            return df, extraction_info
            
        except Exception as e:
            logger.error(f"Error extracting data from {file_path}: {e}")
            return None, {
                'success': False,
                'error': str(e),
                'rows_extracted': 0,
                'columns_found': 0,
                'missing_columns': []
            }
    
    def _extract_excel(self, file_path: str, file_info: Dict[str, Any]) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """Ekstrak data dari file Excel"""
        try:
            # Try different engines for Excel files
            engines = ['openpyxl', 'xlrd']
            df = None
            
            for engine in engines:
                try:
                    df = pd.read_excel(
                        file_path, 
                        header=0, 
                        na_values=['', ' ', '-', 'N/A', 'NULL', 'None'],
                        engine=engine
                    )
                    break
                except Exception as e:
                    logger.warning(f"Engine {engine} failed: {e}")
                    continue
            
            if df is None:
                raise Exception("Semua engine Excel gagal")
            
            # Clean DataFrame
            df = self._clean_dataframe(df)
            
            return df, {
                'extraction_method': 'excel',
                'engine_used': engine if 'engine' in locals() else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error extracting Excel file: {e}")
            return None, {
                'extraction_method': 'excel',
                'error': str(e)
            }
    
    def _extract_text(self, file_path: str, file_info: Dict[str, Any]) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
        """Ekstrak data dari file text"""
        try:
            encoding = file_info.get('encoding', 'utf-8')
            
            # Try different separators
            separators = ['\t', ',', ';', '|']
            df = None
            
            for sep in separators:
                try:
                    df = pd.read_csv(
                        file_path,
                        sep=sep,
                        header=0,
                        encoding=encoding,
                        na_values=['', ' ', '-', 'N/A', 'NULL', 'None']
                    )
                    
                    # Check if we got reasonable number of columns
                    if len(df.columns) > 10:  # Assuming our data has many columns
                        break
                    else:
                        df = None
                        
                except Exception as e:
                    logger.warning(f"Separator {sep} failed: {e}")
                    continue
            
            if df is None:
                raise Exception("Tidak dapat menentukan separator yang tepat")
            
            # Clean DataFrame
            df = self._clean_dataframe(df)
            
            return df, {
                'extraction_method': 'text',
                'separator_used': sep if 'sep' in locals() else 'unknown',
                'encoding_used': encoding
            }
            
        except Exception as e:
            logger.error(f"Error extracting text file: {e}")
            return None, {
                'extraction_method': 'text',
                'error': str(e)
            }
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bersihkan DataFrame"""
        try:
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Remove completely empty columns
            df = df.dropna(axis=1, how='all')
            
            # Strip whitespace from string columns
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            # Replace common null values
            df = df.replace(['None', 'nan', 'NaN', '', ' '], np.nan)
            
            # Reset index
            df = df.reset_index(drop=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning DataFrame: {e}")
            return df

