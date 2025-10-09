"""
Robust Data Extractor Service
Sistem ekstraksi data yang lebih robust dengan validasi integritas
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional, Union
import os
import chardet
from datetime import datetime
import logging
import hashlib
import json

from core.database import db, DataAnalytics, User, UploadLog

logger = logging.getLogger(__name__)

class RobustDataExtractor:
    """
    Service untuk mengekstrak data dengan validasi integritas yang ketat
    """
    
    def __init__(self):
        # Mapping kolom ke tabel database dengan validasi
        self.column_mapping = {
            'data_analytics': {
                'required_columns': ['SEP'],  # Primary key wajib ada
                'optional_columns': [
                    'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF', 'PTD', 'ADMISSION_DATE', 
                    'DISCHARGE_DATE', 'BIRTH_DATE', 'BIRTH_WEIGHT', 'SEX', 'DISCHARGE_STATUS', 
                    'DIAGLIST', 'PROCLIST', 'ADL1', 'ADL2', 'IN_SP', 'IN_SR', 'IN_SI', 'IN_SD', 
                    'INACBG', 'SUBACUTE', 'CHRONIC', 'SP', 'SR', 'SI', 'SD', 'DESKRIPSI_INACBG', 
                    'TARIF_INACBG', 'TARIF_SUBACUTE', 'TARIF_CHRONIC', 'DESKRIPSI_SP', 'TARIF_SP', 
                    'DESKRIPSI_SR', 'TARIF_SR', 'DESKRIPSI_SI', 'TARIF_SI', 'DESKRIPSI_SD', 'TARIF_SD', 
                    'TOTAL_TARIF', 'TARIF_RS', 'TARIF_POLI_EKS', 'LOS', 'ICU_INDIKATOR', 'ICU_LOS', 
                    'VENT_HOUR', 'NAMA_PASIEN', 'MRN', 'UMUR_TAHUN', 'UMUR_HARI', 'DPJP', 
                    'NOKARTU', 'PAYOR_ID', 'CODER_ID', 'VERSI_INACBG', 'VERSI_GROUPER', 'C1', 'C2', 
                    'C3', 'C4', 'PROSEDUR_NON_BEDAH', 'PROSEDUR_BEDAH', 'KONSULTASI', 'TENAGA_AHLI', 
                    'KEPERAWATAN', 'PENUNJANG', 'RADIOLOGI', 'LABORATORIUM', 'PELAYANAN_DARAH', 
                    'REHABILITASI', 'KAMAR_AKOMODASI', 'RAWAT_INTENSIF', 'OBAT', 'ALKES', 'BMHP', 
                    'SEWA_ALAT', 'OBAT_KRONIS', 'OBAT_KEMO'
                ]
            },
            'pasien': {
                'required_columns': ['MRN'],
                'optional_columns': ['NAMA_PASIEN', 'BIRTH_DATE', 'SEX', 'NOKARTU']
            },
            'dokter': {
                'required_columns': ['DPJP'],
                'optional_columns': []
            },
            'diagnosa': {
                'required_columns': ['DIAGLIST'],
                'optional_columns': []
            },
            'prosedur': {
                'required_columns': ['PROCLIST'],
                'optional_columns': []
            }
        }
        
        # Primary keys untuk checking duplikasi
        self.primary_keys = {
            'data_analytics': ['SEP'],
            'pasien': ['MRN'],
            'dokter': ['dokter_id'],
            'diagnosa': ['kode_diagnosa'],
            'prosedur': ['kode_prosedur']
        }
    
    def identify_file_type(self, file_path: str) -> Dict[str, Any]:
        """Identifikasi tipe file dan format"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            file_size = os.path.getsize(file_path)
            
            result = {
                'extension': file_ext,
                'size': file_size,
                'type': 'unknown',
                'encoding': 'utf-8',
                'separator': ',',
                'has_header': True,
                'estimated_rows': 0
            }
            
            # Deteksi tipe file
            if file_ext in ['.xlsx', '.xls']:
                result['type'] = 'excel'
                # Coba baca Excel untuk estimasi
                try:
                    df = pd.read_excel(file_path, nrows=5)
                    result['estimated_rows'] = len(pd.read_excel(file_path))
                    result['columns'] = list(df.columns)
                except Exception as e:
                    logger.warning(f"Error reading Excel file: {e}")
                    
            elif file_ext in ['.csv', '.txt']:
                result['type'] = 'text'
                # Deteksi encoding
                result['encoding'] = self.detect_file_encoding(file_path)
                # Deteksi separator
                result['separator'] = self.detect_separator(file_path, result['encoding'])
                # Estimasi rows
                try:
                    with open(file_path, 'r', encoding=result['encoding']) as f:
                        result['estimated_rows'] = sum(1 for line in f) - 1  # -1 for header
                except Exception as e:
                    logger.warning(f"Error counting rows: {e}")
                    
            return result
            
        except Exception as e:
            logger.error(f"Error identifying file type: {e}")
            return {'type': 'unknown', 'error': str(e)}
    
    def detect_file_encoding(self, file_path: str) -> str:
        """Deteksi encoding file dengan akurasi tinggi"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(50000)  # Baca 50KB pertama
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                
                if confidence > 0.8:
                    return encoding
                else:
                    # Coba encoding umum
                    for enc in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                        try:
                            with open(file_path, 'r', encoding=enc) as f:
                                f.read(1000)
                            return enc
                        except:
                            continue
                    return 'utf-8'
        except Exception as e:
            logger.warning(f"Error detecting encoding: {e}")
            return 'utf-8'
    
    def detect_separator(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Deteksi separator dengan akurasi tinggi"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= 10:  # Baca 10 baris pertama
                        break
                    lines.append(line.strip())
                
                if not lines:
                    return ','
                
                # Hitung kemunculan separator yang umum
                separators = [',', ';', '\t', '|', ' ']
                separator_scores = {}
                
                for sep in separators:
                    score = 0
                    for line in lines:
                        if line:
                            count = line.count(sep)
                            if count > 0:
                                score += count
                    separator_scores[sep] = score
                
                # Pilih separator dengan score tertinggi
                best_separator = max(separator_scores, key=separator_scores.get)
                
                # Jika tidak ada separator yang terdeteksi, gunakan koma
                if separator_scores[best_separator] == 0:
                    return ','
                
                return best_separator
                
        except Exception as e:
            logger.warning(f"Error detecting separator: {e}")
            return ','
    
    def read_file_safely(self, file_path: str, file_info: Dict) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Baca file dengan validasi dan error handling"""
        try:
            df = None
            errors = []
            
            if file_info['type'] == 'excel':
                # Baca Excel file
                try:
                    df = pd.read_excel(file_path)
                    logger.info(f"Successfully read Excel file: {len(df)} rows, {len(df.columns)} columns")
                except Exception as e:
                    errors.append(f"Error reading Excel file: {str(e)}")
                    
            elif file_info['type'] == 'text':
                # Baca text file
                try:
                    df = pd.read_csv(
                        file_path, 
                        encoding=file_info['encoding'], 
                        sep=file_info['separator'],
                        on_bad_lines='skip'  # Skip bad lines
                    )
                    logger.info(f"Successfully read text file: {len(df)} rows, {len(df.columns)} columns")
                except Exception as e:
                    errors.append(f"Error reading text file: {str(e)}")
            
            if df is None or df.empty:
                return None, {'errors': errors, 'message': 'File kosong atau tidak dapat dibaca'}
            
            # Validasi dan cleaning
            df = self.clean_and_validate_dataframe(df)
            
            return df, {'success': True, 'rows': len(df), 'columns': len(df.columns)}
            
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None, {'errors': [str(e)], 'message': 'Error membaca file'}
    
    def clean_and_validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bersihkan dan validasi dataframe"""
        try:
            # Hapus baris kosong
            df = df.dropna(how='all')
            
            # Hapus kolom kosong
            df = df.dropna(axis=1, how='all')
            
            # Strip whitespace dari string columns
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            # Replace nilai kosong dengan None
            df = df.replace(['None', 'nan', 'NaN', '', ' ', 'null', 'NULL'], None)
            
            # Validasi primary key (SEP) jika ada
            if 'SEP' in df.columns:
                # Hapus baris dengan SEP kosong
                df = df.dropna(subset=['SEP'])
                # Hapus duplikasi SEP dalam file
                df = df.drop_duplicates(subset=['SEP'], keep='first')
            
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning dataframe: {e}")
            return df
    
    def validate_data_integrity(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validasi integritas data"""
        try:
            validation_result = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'row_hashes': {},
                'integrity_score': 100
            }
            
            if df.empty:
                validation_result['is_valid'] = False
                validation_result['errors'].append('Data kosong')
                return validation_result
            
            # Validasi primary key
            if 'SEP' in df.columns:
                # Cek duplikasi SEP
                duplicate_seps = df[df.duplicated(subset=['SEP'], keep=False)]['SEP'].tolist()
                if duplicate_seps:
                    validation_result['warnings'].append(f'Duplikasi SEP dalam file: {duplicate_seps}')
                    validation_result['integrity_score'] -= 10
                
                # Cek SEP kosong
                empty_seps = df[df['SEP'].isna() | (df['SEP'] == '')].index.tolist()
                if empty_seps:
                    validation_result['errors'].append(f'SEP kosong pada baris: {empty_seps}')
                    validation_result['integrity_score'] -= 20
                    validation_result['is_valid'] = False
            
            # Buat hash untuk setiap baris untuk validasi integritas
            for idx, row in df.iterrows():
                row_data = row.to_dict()
                # Buat hash dari data baris
                row_hash = hashlib.md5(json.dumps(row_data, sort_keys=True).encode()).hexdigest()
                validation_result['row_hashes'][idx] = row_hash
            
            # Validasi konsistensi data
            if 'NAMA_PASIEN' in df.columns and 'MRN' in df.columns:
                # Cek konsistensi nama pasien dengan MRN
                inconsistent_data = df.groupby('MRN')['NAMA_PASIEN'].nunique()
                inconsistent_mrns = inconsistent_data[inconsistent_data > 1].index.tolist()
                if inconsistent_mrns:
                    validation_result['warnings'].append(f'MRN dengan nama pasien berbeda: {inconsistent_mrns}')
                    validation_result['integrity_score'] -= 15
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating data integrity: {e}")
            return {
                'is_valid': False,
                'errors': [str(e)],
                'warnings': [],
                'row_hashes': {},
                'integrity_score': 0
            }
    
    def check_database_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check duplikasi dengan database"""
        try:
            duplicate_result = {
                'new_records': [],
                'duplicate_records': [],
                'total_new': 0,
                'total_duplicates': 0
            }
            
            if 'SEP' in df.columns:
                # Check duplikasi SEP dengan database
                existing_seps = set()
                try:
                    existing_data = DataAnalytics.query.with_entities(DataAnalytics.sep).all()
                    existing_seps = {row.sep for row in existing_data}
                except Exception as e:
                    logger.warning(f"Error checking existing SEPs: {e}")
                
                for idx, row in df.iterrows():
                    sep_value = row.get('SEP')
                    if sep_value and sep_value in existing_seps:
                        duplicate_result['duplicate_records'].append({
                            'row_index': idx,
                            'sep': sep_value,
                            'reason': 'SEP sudah ada di database'
                        })
                        logger.info(f"Duplicate found: SEP {sep_value} at row {idx}")
                    else:
                        duplicate_result['new_records'].append({
                            'row_index': idx,
                            'sep': sep_value
                        })
                        logger.info(f"New record: SEP {sep_value} at row {idx}")
                
                duplicate_result['total_new'] = len(duplicate_result['new_records'])
                duplicate_result['total_duplicates'] = len(duplicate_result['duplicate_records'])
            
            return duplicate_result
            
        except Exception as e:
            logger.error(f"Error checking database duplicates: {e}")
            return {
                'new_records': [],
                'duplicate_records': [],
                'total_new': 0,
                'total_duplicates': 0,
                'error': str(e)
            }
    
    def insert_data_with_integrity(self, df: pd.DataFrame, duplicate_info: Dict, user_id: int) -> Dict[str, Any]:
        """Insert data dengan menjaga integritas"""
        try:
            insert_result = {
                'success': True,
                'inserted_rows': 0,
                'failed_rows': 0,
                'errors': [],
                'table_results': {}
            }
            
            # Insert ke data_analytics
            if 'SEP' in df.columns:
                inserted_count = 0
                failed_count = 0
                
                for record in duplicate_info['new_records']:
                    try:
                        row_idx = record['row_index']
                        row_data = df.iloc[row_idx].to_dict()
                        
                        # Konversi data ke format yang sesuai
                        clean_data = self.prepare_data_for_insert(row_data)
                        
                        # Insert ke database
                        data_analytics = DataAnalytics(**clean_data)
                        db.session.add(data_analytics)
                        db.session.commit()
                        
                        inserted_count += 1
                        
                    except Exception as e:
                        db.session.rollback()
                        failed_count += 1
                        insert_result['errors'].append(f"Baris {row_idx}: {str(e)}")
                        logger.error(f"Error inserting row {row_idx}: {e}")
                
                insert_result['table_results']['data_analytics'] = {
                    'inserted': inserted_count,
                    'failed': failed_count
                }
                insert_result['inserted_rows'] += inserted_count
                insert_result['failed_rows'] += failed_count
            
            
            return insert_result
            
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            db.session.rollback()
            return {
                'success': False,
                'inserted_rows': 0,
                'failed_rows': 0,
                'errors': [str(e)],
                'table_results': {}
            }
    
    def prepare_data_for_insert(self, row_data: Dict) -> Dict:
        """Persiapkan data untuk insert ke database"""
        try:
            clean_data = {}
            
            # Mapping kolom ke nama database
            column_mapping = {
                'SEP': 'sep',
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
            
            for source_col, target_col in column_mapping.items():
                if source_col in row_data and row_data[source_col] is not None:
                    value = row_data[source_col]
                    
                    # Konversi tipe data
                    if target_col in ['ptd', 'sex', 'discharge_status', 'los', 'icu_indikator', 'icu_los', 'vent_hour', 'umur_tahun', 'umur_hari']:
                        try:
                            clean_data[target_col] = int(value) if value else None
                        except:
                            clean_data[target_col] = None
                    elif target_col in ['birth_weight']:
                        try:
                            clean_data[target_col] = float(value) if value else None
                        except:
                            clean_data[target_col] = None
                    elif target_col in ['tarif_inacbg', 'tarif_subacute', 'tarif_chronic', 'tarif_sp', 'tarif_sr', 'tarif_si', 'tarif_sd', 'total_tarif', 'tarif_rs', 'tarif_poli_eks', 'prosedur_non_bedah', 'prosedur_bedah', 'konsultasi', 'tenaga_ahli', 'keperawatan', 'penunjang', 'radiologi', 'laboratorium', 'pelayanan_darah', 'rehabilitasi', 'kamar_akomodasi', 'rawat_intensif', 'obat', 'alkes', 'bmhp', 'sewa_alat', 'obat_kronis', 'obat_kemo']:
                        try:
                            clean_data[target_col] = int(float(value)) if value else None
                        except:
                            clean_data[target_col] = None
                    else:
                        clean_data[target_col] = str(value) if value else None
            
            return clean_data
            
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            return {}
    
    
    def parse_date(self, date_value) -> Optional[datetime]:
        """Parse date value ke datetime"""
        if not date_value:
            return None
        
        try:
            if isinstance(date_value, datetime):
                return date_value
            elif isinstance(date_value, str):
                # Coba berbagai format date
                formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y%m%d', '%d-%m-%Y']
                for fmt in formats:
                    try:
                        return datetime.strptime(date_value, fmt)
                    except ValueError:
                        continue
            elif isinstance(date_value, (int, float)):
                # Excel date serial number
                return datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(date_value) - 2)
            
            return None
        except Exception:
            return None
    
    def process_file_complete(self, file_path: str, user_id: int) -> Dict[str, Any]:
        """Proses file lengkap dengan validasi integritas"""
        try:
            result = {
                'success': False,
                'message': '',
                'file_info': {},
                'validation': {},
                'duplicate_check': {},
                'insert_result': {},
                'summary': {}
            }
            
            # 1. Identifikasi file
            file_info = self.identify_file_type(file_path)
            result['file_info'] = file_info
            
            if file_info.get('type') == 'unknown':
                result['message'] = 'Tipe file tidak dikenali'
                return result
            
            # 2. Baca file
            df, read_result = self.read_file_safely(file_path, file_info)
            if df is None:
                result['message'] = read_result.get('message', 'Error membaca file')
                result['errors'] = read_result.get('errors', [])
                return result
            
            # 3. Validasi integritas data
            validation = self.validate_data_integrity(df)
            result['validation'] = validation
            
            if not validation['is_valid']:
                result['message'] = 'Data tidak valid: ' + ', '.join(validation['errors'])
                return result
            
            # 4. Check duplikasi dengan database
            duplicate_check = self.check_database_duplicates(df)
            result['duplicate_check'] = duplicate_check
            
            # 5. Insert data
            insert_result = self.insert_data_with_integrity(df, duplicate_check, user_id)
            result['insert_result'] = insert_result
            
            # 6. Buat summary
            result['summary'] = {
                'total_rows': len(df),
                'new_rows': duplicate_check['total_new'],
                'duplicate_rows': duplicate_check['total_duplicates'],
                'inserted_rows': insert_result['inserted_rows'],
                'failed_rows': insert_result['failed_rows'],
                'duplicate_failed_rows': duplicate_check['total_duplicates'],  # Baris yang gagal karena duplikat
                'insert_failed_rows': insert_result['failed_rows'],  # Baris yang gagal karena error insert
                'total_failed_rows': duplicate_check['total_duplicates'] + insert_result['failed_rows'],  # Total baris yang gagal
                'success_rows': insert_result['inserted_rows'],  # Baris yang berhasil diinsert
                'integrity_score': validation['integrity_score']
            }
            
            # Log summary for debugging
            logger.info(f"Upload summary: Total={result['summary']['total_rows']}, "
                       f"Success={result['summary']['success_rows']}, "
                       f"Failed={result['summary']['total_failed_rows']} "
                       f"(Duplicates={result['summary']['duplicate_failed_rows']}, "
                       f"Insert errors={result['summary']['insert_failed_rows']})")
            
            if insert_result['success']:
                result['success'] = True
                if duplicate_check['total_duplicates'] > 0 and insert_result['inserted_rows'] > 0:
                    result['message'] = f"Data diproses: {insert_result['inserted_rows']} baris berhasil, {duplicate_check['total_duplicates']} baris duplikat (gagal)"
                elif duplicate_check['total_duplicates'] > 0:
                    result['message'] = f"Semua {duplicate_check['total_duplicates']} baris adalah duplikat (gagal)"
                else:
                    result['message'] = f"Data berhasil diproses: {insert_result['inserted_rows']} baris baru"
            else:
                result['message'] = f"Error memproses data: {', '.join(insert_result['errors'])}"
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return {
                'success': False,
                'message': f'Error memproses file: {str(e)}',
                'file_info': {},
                'validation': {},
                'duplicate_check': {},
                'insert_result': {},
                'summary': {}
            }

