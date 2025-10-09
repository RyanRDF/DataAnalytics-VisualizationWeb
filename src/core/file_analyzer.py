"""
File Analyzer untuk menganalisa tipe file dan menentukan ekstraktor yang sesuai
"""
import os
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class FileAnalyzer:
    """Class untuk menganalisa file dan menentukan tipe ekstraksi"""
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.xlsx', '.xls']
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analisa file dan return informasi file
        
        Args:
            file_path: Path ke file yang akan dianalisa
            
        Returns:
            Dict dengan informasi file
        """
        try:
            file_info = {
                'file_path': file_path,
                'filename': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'file_type': None,
                'extension': None,
                'is_supported': False,
                'encoding': None,
                'error': None
            }
            
            # Get file extension
            _, ext = os.path.splitext(file_path)
            file_info['extension'] = ext.lower()
            
            # Check if supported
            if ext.lower() in self.supported_extensions:
                file_info['is_supported'] = True
                
                # Determine file type
                if ext.lower() in ['.xlsx', '.xls']:
                    file_info['file_type'] = 'excel'
                elif ext.lower() == '.txt':
                    file_info['file_type'] = 'text'
                    # Detect encoding for text files
                    file_info['encoding'] = self._detect_encoding(file_path)
            else:
                file_info['error'] = f'File type {ext} tidak didukung. Hanya mendukung: {", ".join(self.supported_extensions)}'
            
            logger.info(f"File analyzed: {file_info['filename']} - Type: {file_info['file_type']}")
            return file_info
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return {
                'file_path': file_path,
                'filename': os.path.basename(file_path),
                'error': str(e),
                'is_supported': False
            }
    
    def _detect_encoding(self, file_path: str) -> str:
        """Deteksi encoding file text"""
        try:
            import chardet
            
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8')
        except Exception:
            return 'utf-8'  # Default encoding
    
    def get_extractor_type(self, file_info: Dict[str, Any]) -> str:
        """
        Tentukan tipe ekstraktor berdasarkan file info
        
        Args:
            file_info: Informasi file dari analyze_file
            
        Returns:
            String tipe ekstraktor ('excel' atau 'text')
        """
        if not file_info.get('is_supported'):
            raise ValueError(f"File tidak didukung: {file_info.get('error', 'Unknown error')}")
        
        return file_info['file_type']

