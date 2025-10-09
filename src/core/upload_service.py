"""
Upload Service untuk mengelola proses upload file dengan alur yang terstruktur
"""
import os
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

from core.file_analyzer import FileAnalyzer
from core.data_extractor import DataExtractor
from core.dataframe_manager import DataFrameManager
from core.duplicate_checker import DuplicateChecker
from core.database import db, DataAnalytics, UploadLog
from utils.timezone_utils import jakarta_now

logger = logging.getLogger(__name__)

class UploadService:
    """Service untuk mengelola proses upload file"""
    
    def __init__(self):
        self.file_analyzer = FileAnalyzer()
        self.data_extractor = DataExtractor()
        self.dataframe_manager = DataFrameManager()
        self.duplicate_checker = DuplicateChecker()
    
    def process_upload(self, file_path: str, user_id: int) -> Dict[str, Any]:
        """
        Proses upload file dengan alur yang terstruktur
        
        Args:
            file_path: Path ke file yang akan diupload
            user_id: ID user yang melakukan upload
            
        Returns:
            Dict dengan hasil upload
        """
        try:
            logger.info(f"Starting upload process for file: {file_path}")
            
            # Step 1: Analisa file
            file_info = self.file_analyzer.analyze_file(file_path)
            if not file_info.get('is_supported'):
                return {
                    'success': False,
                    'error': file_info.get('error', 'File tidak didukung'),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 2: Ekstraksi data ke DataFrame
            df, extraction_info = self.data_extractor.extract_data(file_path, file_info)
            if df is None or df.empty:
                return {
                    'success': False,
                    'error': extraction_info.get('error', 'Gagal mengekstrak data'),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 3: Set DataFrame ke manager
            df_info = self.dataframe_manager.set_dataframe(df)
            if not df_info.get('success'):
                return {
                    'success': False,
                    'error': df_info.get('error', 'Gagal mengatur DataFrame'),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 4: Validasi DataFrame
            validation_result = self.dataframe_manager.validate_dataframe()
            if not validation_result.get('is_valid'):
                return {
                    'success': False,
                    'error': '; '.join(validation_result.get('errors', ['Validasi gagal'])),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 5: Cek duplikasi
            duplicate_result = self.duplicate_checker.check_duplicates(df)
            if not duplicate_result.get('success'):
                return {
                    'success': False,
                    'error': duplicate_result.get('error', 'Gagal mengecek duplikasi'),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 6: Pisahkan data valid dan duplikat
            separation_result = self.dataframe_manager.separate_valid_duplicate_data(
                self.duplicate_checker.get_existing_seps()
            )
            if not separation_result.get('success'):
                return {
                    'success': False,
                    'error': separation_result.get('error', 'Gagal memisahkan data'),
                    'rows_success': 0,
                    'rows_failed': 0
                }
            
            # Step 7: Upload data valid ke database
            upload_result = self._upload_valid_data(user_id, file_path)
            
            # Step 8: Log upload ke database
            log_result = self._log_upload(
                user_id, 
                file_path, 
                separation_result['valid_rows'],
                separation_result['duplicate_rows'],
                upload_result.get('success', False),
                upload_result.get('error')
            )
            
            # Step 9: Clear DataFrame
            self.dataframe_manager.clear_dataframe()
            
            # Prepare final result
            final_result = {
                'success': upload_result.get('success', False),
                'rows_success': separation_result['valid_rows'] if upload_result.get('success') else 0,
                'rows_failed': separation_result['duplicate_rows'],
                'total_rows': separation_result['total_rows'],
                'message': self._generate_message(separation_result, upload_result),
                'file_info': file_info,
                'extraction_info': extraction_info,
                'validation_result': validation_result,
                'duplicate_result': duplicate_result,
                'upload_result': upload_result,
                'log_result': log_result
            }
            
            logger.info(f"Upload process completed: {final_result}")
            return final_result
            
        except Exception as e:
            logger.error(f"Error in upload process: {e}")
            return {
                'success': False,
                'error': str(e),
                'rows_success': 0,
                'rows_failed': 0
            }
    
    def _upload_valid_data(self, user_id: int, file_path: str) -> Dict[str, Any]:
        """
        Upload data valid ke database
        
        Args:
            user_id: ID user
            file_path: Path file
            
        Returns:
            Dict dengan hasil upload
        """
        try:
            valid_data = self.dataframe_manager.get_valid_data()
            
            if valid_data is None or valid_data.empty:
                return {
                    'success': True,
                    'inserted_rows': 0,
                    'message': 'Tidak ada data valid untuk diupload'
                }
            
            # Convert DataFrame to list of dictionaries
            data_list = valid_data.to_dict('records')
            
            # Insert data to database
            inserted_count = 0
            errors = []
            
            for row_data in data_list:
                try:
                    # Map column names from uppercase to lowercase for database
                    mapped_data = self._map_column_names(row_data)
                    
                    # Create DataAnalytics object
                    data_analytics = DataAnalytics(**mapped_data)
                    db.session.add(data_analytics)
                    inserted_count += 1
                except Exception as e:
                    errors.append(f"Row error: {str(e)}")
                    logger.warning(f"Error inserting row: {e}")
            
            # Commit transaction
            if inserted_count > 0:
                db.session.commit()
                logger.info(f"Successfully inserted {inserted_count} rows to database")
            
            return {
                'success': True,
                'inserted_rows': inserted_count,
                'errors': errors,
                'message': f'Berhasil mengupload {inserted_count} baris data'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error uploading valid data: {e}")
            return {
                'success': False,
                'error': str(e),
                'inserted_rows': 0
            }
    
    def _log_upload(self, user_id: int, file_path: str, rows_success: int, 
                   rows_failed: int, upload_success: bool, error_message: str = None) -> Dict[str, Any]:
        """
        Log upload ke database
        
        Args:
            user_id: ID user
            file_path: Path file
            rows_success: Jumlah baris berhasil
            rows_failed: Jumlah baris gagal
            upload_success: Status upload
            error_message: Pesan error jika ada
            
        Returns:
            Dict dengan hasil logging
        """
        try:
            upload_log = UploadLog(
                user_id=user_id,
                filename=os.path.basename(file_path),
                file_path=file_path,
                file_size=os.path.getsize(file_path),
                rows_processed=rows_success + rows_failed,
                rows_success=rows_success,
                rows_failed=rows_failed,
                upload_time=jakarta_now(),
                status='success' if upload_success else 'failed',
                error_message=error_message
            )
            
            db.session.add(upload_log)
            db.session.commit()
            
            logger.info(f"Upload logged: {rows_success} success, {rows_failed} failed")
            return {
                'success': True,
                'log_id': upload_log.id
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error logging upload: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _map_column_names(self, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map column names from uppercase (file) to lowercase (database)
        
        Args:
            row_data: Dictionary with uppercase column names
            
        Returns:
            Dictionary with lowercase column names
        """
        column_mapping = {
            'KODE_RS': 'kode_rs',
            'KELAS_RS': 'kelas_rs',
            'KELAS_RAWAT': 'kelas_rawat',
            'KODE_TARIF': 'kode_tarif',
            'PTD': 'ptd',
            'ADMISSION_DATE': 'admission_date',
            'DISCHARGE_DATE': 'discharge_date',
            'BIRTH_DATE': 'birth_date',
            'BIRTH_WEIGHT': 'birth_weight',
            'SEX': 'sex',
            'DISCHARGE_STATUS': 'discharge_status',
            'DIAGLIST': 'diaglist',
            'PROCLIST': 'proclist',
            'ADL1': 'adl1',
            'ADL2': 'adl2',
            'IN_SP': 'in_sp',
            'IN_SR': 'in_sr',
            'IN_SI': 'in_si',
            'IN_SD': 'in_sd',
            'INACBG': 'inacbg',
            'SUBACUTE': 'subacute',
            'CHRONIC': 'chronic',
            'SP': 'sp',
            'SR': 'sr',
            'SI': 'si',
            'SD': 'sd',
            'DESKRIPSI_INACBG': 'deskripsi_inacbg',
            'TARIF_INACBG': 'tarif_inacbg',
            'TARIF_SUBACUTE': 'tarif_subacute',
            'TARIF_CHRONIC': 'tarif_chronic',
            'DESKRIPSI_SP': 'deskripsi_sp',
            'TARIF_SP': 'tarif_sp',
            'DESKRIPSI_SR': 'deskripsi_sr',
            'TARIF_SR': 'tarif_sr',
            'DESKRIPSI_SI': 'deskripsi_si',
            'TARIF_SI': 'tarif_si',
            'DESKRIPSI_SD': 'deskripsi_sd',
            'TARIF_SD': 'tarif_sd',
            'TOTAL_TARIF': 'total_tarif',
            'TARIF_RS': 'tarif_rs',
            'TARIF_POLI_EKS': 'tarif_poli_eks',
            'LOS': 'los',
            'ICU_INDIKATOR': 'icu_indikator',
            'ICU_LOS': 'icu_los',
            'VENT_HOUR': 'vent_hour',
            'NAMA_PASIEN': 'nama_pasien',
            'MRN': 'mrn',
            'UMUR_TAHUN': 'umur_tahun',
            'UMUR_HARI': 'umur_hari',
            'DPJP': 'dpjp',
            'SEP': 'sep',
            'NOKARTU': 'nokartu',
            'PAYOR_ID': 'payor_id',
            'CODER_ID': 'coder_id',
            'VERSI_INACBG': 'versi_inacbg',
            'VERSI_GROUPER': 'versi_grouper',
            'C1': 'c1',
            'C2': 'c2',
            'C3': 'c3',
            'C4': 'c4',
            'PROSEDUR_NON_BEDAH': 'prosedur_non_bedah',
            'PROSEDUR_BEDAH': 'prosedur_bedah',
            'KONSULTASI': 'konsultasi',
            'TENAGA_AHLI': 'tenaga_ahli',
            'KEPERAWATAN': 'keperawatan',
            'PENUNJANG': 'penunjang',
            'RADIOLOGI': 'radiologi',
            'LABORATORIUM': 'laboratorium',
            'PELAYANAN_DARAH': 'pelayanan_darah',
            'REHABILITASI': 'rehabilitasi',
            'KAMAR_AKOMODASI': 'kamar_akomodasi',
            'RAWAT_INTENSIF': 'rawat_intensif',
            'OBAT': 'obat',
            'ALKES': 'alkes',
            'BMHP': 'bmhp',
            'SEWA_ALAT': 'sewa_alat',
            'OBAT_KRONIS': 'obat_kronis',
            'OBAT_KEMO': 'obat_kemo'
        }
        
        mapped_data = {}
        for key, value in row_data.items():
            if key in column_mapping:
                mapped_data[column_mapping[key]] = value
            else:
                # If no mapping found, use lowercase version
                mapped_data[key.lower()] = value
        
        return mapped_data

    def _generate_message(self, separation_result: Dict[str, Any], upload_result: Dict[str, Any]) -> str:
        """Generate pesan berdasarkan hasil upload"""
        valid_rows = separation_result.get('valid_rows', 0)
        duplicate_rows = separation_result.get('duplicate_rows', 0)
        
        if upload_result.get('success'):
            if valid_rows > 0 and duplicate_rows > 0:
                return f"Data diproses: {valid_rows} baris berhasil, {duplicate_rows} baris duplikat (gagal)"
            elif valid_rows > 0:
                return f"Data berhasil diproses: {valid_rows} baris baru"
            elif duplicate_rows > 0:
                return f"Semua {duplicate_rows} baris adalah duplikat (gagal)"
            else:
                return "Tidak ada data untuk diproses"
        else:
            return f"Error memproses data: {upload_result.get('error', 'Unknown error')}"
