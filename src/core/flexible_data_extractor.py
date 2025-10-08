"""
Flexible Data Extractor Service
Mengekstrak data dari berbagai format file dan memetakan ke tabel database yang sesuai
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
import os
import chardet
from datetime import datetime
import logging

from core.database import db, DataAnalytics, Pasien, Kunjungan, KunjunganDiagnosa, KunjunganProsedur, \
                         Dokter, Diagnosa, Prosedur, User, UploadLog

logger = logging.getLogger(__name__)

class FlexibleDataExtractor:
    """
    Service untuk mengekstrak data dari berbagai format file dan memetakan ke database
    """
    
    def __init__(self):
        # Mapping kolom ke tabel database
        self.column_mapping = {
            # Tabel utama data_analytics
            'data_analytics': [
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
            ],
            
            # Tabel ERD yang tersedia
            'pasien': ['MRN', 'NAMA_PASIEN', 'BIRTH_DATE', 'SEX', 'NOKARTU'],
            'dokter': ['DPJP'],
            'diagnosa': ['DIAGLIST'],
            'prosedur': ['PROCLIST']
        }
        
        # Primary keys untuk checking duplikasi
        self.primary_keys = {
            'data_analytics': ['SEP'],
            'pasien': ['MRN'],
            'dokter': ['dokter_id'],  # Auto-increment
            'diagnosa': ['kode_diagnosa'],
            'prosedur': ['kode_prosedur']
        }
    
    def detect_file_encoding(self, file_path: str) -> str:
        """Deteksi encoding file"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Baca 10KB pertama
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                confidence = result['confidence']
                
                if confidence > 0.7:
                    return encoding
                else:
                    return 'utf-8'  # Default fallback
        except Exception as e:
            logger.warning(f"Error detecting encoding: {e}")
            return 'utf-8'
    
    def detect_separator(self, file_path: str, encoding: str = 'utf-8') -> str:
        """Deteksi separator file"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # Baca beberapa baris pertama
                lines = []
                for i, line in enumerate(f):
                    if i >= 5:  # Baca maksimal 5 baris
                        break
                    lines.append(line.strip())
                
                if not lines:
                    return ','
                
                # Hitung kemunculan separator yang umum
                separators = [',', ';', '\t', '|']
                separator_counts = {}
                
                for sep in separators:
                    count = 0
                    for line in lines:
                        count += line.count(sep)
                    separator_counts[sep] = count
                
                # Pilih separator dengan count tertinggi
                best_separator = max(separator_counts, key=separator_counts.get)
                
                # Jika tidak ada separator yang terdeteksi, gunakan koma
                if separator_counts[best_separator] == 0:
                    return ','
                
                return best_separator
                
        except Exception as e:
            logger.warning(f"Error detecting separator: {e}")
            return ','
    
    def read_file(self, file_path: str) -> pd.DataFrame:
        """Baca file dengan deteksi otomatis format dan separator"""
        try:
            # Deteksi encoding
            encoding = self.detect_file_encoding(file_path)
            logger.info(f"Detected encoding: {encoding}")
            
            # Deteksi separator
            separator = self.detect_separator(file_path, encoding)
            logger.info(f"Detected separator: '{separator}'")
            
            # Baca file berdasarkan ekstensi
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.xlsx', '.xls']:
                # Excel file
                df = pd.read_excel(file_path)
            elif file_ext == '.csv':
                # CSV file
                df = pd.read_csv(file_path, encoding=encoding, sep=separator)
            elif file_ext == '.txt':
                # Text file
                df = pd.read_csv(file_path, encoding=encoding, sep=separator)
            else:
                # Default: coba sebagai CSV
                df = pd.read_csv(file_path, encoding=encoding, sep=separator)
            
            # Clean data
            df = self.clean_dataframe(df)
            
            logger.info(f"Successfully read file: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bersihkan dataframe"""
        # Hapus baris kosong
        df = df.dropna(how='all')
        
        # Hapus kolom kosong
        df = df.dropna(axis=1, how='all')
        
        # Strip whitespace dari string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Replace 'None', 'nan', 'NaN' dengan None
        df = df.replace(['None', 'nan', 'NaN', ''], None)
        
        return df
    
    def check_duplicates(self, table_name: str, data: List[Dict], primary_keys: List[str]) -> Tuple[List[Dict], List[Dict]]:
        """Check duplikasi data berdasarkan primary key"""
        try:
            new_data = []
            duplicates = []
            
            for row in data:
                # Buat kondisi untuk query
                conditions = []
                for pk in primary_keys:
                    if pk in row and row[pk] is not None:
                        conditions.append(getattr(globals()[table_name.title()], pk) == row[pk])
                
                if not conditions:
                    # Jika tidak ada primary key, anggap sebagai data baru
                    new_data.append(row)
                    continue
                
                # Query untuk check duplikasi
                existing = globals()[table_name.title()].query.filter(*conditions).first()
                
                if existing:
                    duplicates.append(row)
                else:
                    new_data.append(row)
            
            return new_data, duplicates
            
        except Exception as e:
            logger.error(f"Error checking duplicates for {table_name}: {e}")
            return data, []
    
    def extract_data_to_tables(self, df: pd.DataFrame, user_id: int) -> Dict[str, Any]:
        """Ekstrak data ke berbagai tabel database"""
        try:
            results = {
                'total_rows': len(df),
                'processed_rows': 0,
                'duplicate_rows': 0,
                'error_rows': 0,
                'table_results': {},
                'errors': []
            }
            
            # Konversi dataframe ke list of dicts
            data_list = df.to_dict('records')
            
            # Proses setiap tabel
            for table_name, columns in self.column_mapping.items():
                try:
                    # Filter data yang memiliki kolom yang sesuai
                    table_data = []
                    for row in data_list:
                        filtered_row = {}
                        has_data = False
                        
                        for col in columns:
                            if col in row and row[col] is not None and str(row[col]).strip():
                                filtered_row[col] = row[col]
                                has_data = True
                        
                        if has_data:
                            table_data.append(filtered_row)
                    
                    if not table_data:
                        continue
                    
                    # Check duplikasi
                    primary_keys = self.primary_keys.get(table_name, [])
                    new_data, duplicates = self.check_duplicates(table_name, table_data, primary_keys)
                    
                    # Insert data baru
                    inserted_count = 0
                    for row in new_data:
                        try:
                            if table_name == 'data_analytics':
                                self.insert_data_analytics(row)
                            elif table_name == 'pasien':
                                self.insert_pasien(row)
                            elif table_name == 'dokter':
                                self.insert_dokter(row)
                            elif table_name == 'diagnosa':
                                self.insert_diagnosa(row)
                            elif table_name == 'prosedur':
                                self.insert_prosedur(row)
                            
                            inserted_count += 1
                            
                        except Exception as e:
                            logger.error(f"Error inserting row to {table_name}: {e}")
                            results['error_rows'] += 1
                            results['errors'].append(f"{table_name}: {str(e)}")
                    
                    # Update results
                    results['table_results'][table_name] = {
                        'total': len(table_data),
                        'inserted': inserted_count,
                        'duplicates': len(duplicates)
                    }
                    
                    results['processed_rows'] += inserted_count
                    results['duplicate_rows'] += len(duplicates)
                    
                except Exception as e:
                    logger.error(f"Error processing table {table_name}: {e}")
                    results['errors'].append(f"{table_name}: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            raise
    
    def insert_data_analytics(self, row: Dict):
        """Insert data ke tabel data_analytics"""
        data = DataAnalytics(**row)
        db.session.add(data)
        db.session.commit()
    
    def insert_pasien(self, row: Dict):
        """Insert data ke tabel pasien"""
        data = Pasien(
            mrn=row.get('MRN'),
            nama_pasien=row.get('NAMA_PASIEN'),
            birth_date=self.parse_date(row.get('BIRTH_DATE')),
            sex=row.get('SEX'),
            nokartu=row.get('NOKARTU')
        )
        db.session.add(data)
        db.session.commit()
    
    def insert_dokter(self, row: Dict):
        """Insert data ke tabel dokter"""
        data = Dokter(
            nama_dokter=row.get('DPJP')
        )
        db.session.add(data)
        db.session.commit()
    
    def insert_diagnosa(self, row: Dict):
        """Insert data ke tabel diagnosa"""
        # Parse DIAGLIST untuk mendapatkan kode diagnosa
        diaglist = row.get('DIAGLIST', '')
        if diaglist and isinstance(diaglist, str):
            # Format: "1 A09.9" -> ambil "A09.9"
            parts = diaglist.split()
            if len(parts) > 1:
                kode = parts[1]
                data = Diagnosa(
                    kode_diagnosa=kode,
                    deskripsi=diaglist
                )
                db.session.add(data)
                db.session.commit()
    
    def insert_prosedur(self, row: Dict):
        """Insert data ke tabel prosedur"""
        # Parse PROCLIST untuk mendapatkan kode prosedur
        proclist = row.get('PROCLIST', '')
        if proclist and isinstance(proclist, str):
            # Format: "79.02" atau "1 79.02" -> ambil kode
            parts = proclist.split()
            if len(parts) > 1:
                kode = parts[1]
            else:
                kode = parts[0]
            
            data = Prosedur(
                kode_prosedur=kode,
                deskripsi=proclist
            )
            db.session.add(data)
            db.session.commit()
    
    
    def parse_date(self, date_value) -> Optional[datetime]:
        """Parse date value ke datetime"""
        if not date_value:
            return None
        
        try:
            if isinstance(date_value, datetime):
                return date_value
            elif isinstance(date_value, str):
                # Coba berbagai format date
                formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y%m%d']
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
    
    def parse_numeric(self, value) -> Optional[float]:
        """Parse numeric value"""
        if not value:
            return None
        
        try:
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                # Remove non-numeric characters except decimal point
                cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
                return float(cleaned) if cleaned else None
            return None
        except Exception:
            return None
    
    def process_file(self, file_path: str, user_id: int) -> Dict[str, Any]:
        """Proses file lengkap dari ekstraksi sampai insert ke database"""
        try:
            # Baca file
            df = self.read_file(file_path)
            
            if df.empty:
                return {
                    'success': False,
                    'message': 'File kosong atau tidak dapat dibaca',
                    'stats': {}
                }
            
            # Ekstrak data ke tabel
            results = self.extract_data_to_tables(df, user_id)
            
            # Buat summary
            summary = {
                'total_rows': results['total_rows'],
                'processed_rows': results['processed_rows'],
                'duplicate_rows': results['duplicate_rows'],
                'error_rows': results['error_rows'],
                'table_breakdown': results['table_results']
            }
            
            return {
                'success': True,
                'message': f'Data berhasil diproses: {results["processed_rows"]} baris baru, {results["duplicate_rows"]} duplikat',
                'stats': summary,
                'errors': results['errors']
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return {
                'success': False,
                'message': f'Error memproses file: {str(e)}',
                'stats': {}
            }
