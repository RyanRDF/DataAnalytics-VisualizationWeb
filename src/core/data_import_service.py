"""
Data Import Service for importing file data to database
"""
import pandas as pd
import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from .database import db, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur


class DataImportService:
    """Service for importing data from files to database"""
    
    def __init__(self):
        self.import_stats = {
            'total_rows': 0,
            'imported_pasien': 0,
            'imported_dokter': 0,
            'imported_diagnosa': 0,
            'imported_prosedur': 0,
            'imported_kunjungan': 0,
            'imported_rincian_biaya': 0,
            'imported_kunjungan_diagnosa': 0,
            'imported_kunjungan_prosedur': 0,
            'errors': []
        }
    
    def import_file_to_database(self, filepath: str) -> Dict[str, Any]:
        """
        Import data from file to database
        
        Args:
            filepath: Path to the uploaded file
            
        Returns:
            Dictionary with import results
        """
        try:
            # Reset stats
            self.import_stats = {
                'total_rows': 0,
                'imported_pasien': 0,
                'imported_dokter': 0,
                'imported_diagnosa': 0,
                'imported_prosedur': 0,
                'imported_kunjungan': 0,
                'imported_rincian_biaya': 0,
                'imported_kunjungan_diagnosa': 0,
                'imported_kunjungan_prosedur': 0,
                'errors': []
            }
            
            # Read file
            df = pd.read_csv(filepath, sep='\t')
            self.import_stats['total_rows'] = len(df)
            
            # Validate data
            validation_result = self.validate_file_data(df)
            if not validation_result['is_valid']:
                return {
                    'success': False,
                    'error': f"Data validation failed: {validation_result['error']}",
                    'stats': self.import_stats
                }
            
            # Import data in batches
            batch_size = 100
            for i in range(0, len(df), batch_size):
                batch_df = df.iloc[i:i+batch_size]
                self._import_batch(batch_df)
            
            return {
                'success': True,
                'message': f"Successfully imported {self.import_stats['total_rows']} rows",
                'stats': self.import_stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Import failed: {str(e)}",
                'stats': self.import_stats
            }
    
    def validate_file_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate file data before import
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        required_columns = [
            'KODE_RS', 'KELAS_RS', 'KELAS_RAWAT', 'KODE_TARIF',
            'ADMISSION_DATE', 'DISCHARGE_DATE', 'BIRTH_DATE', 'SEX',
            'NAMA_PASIEN', 'MRN', 'DPJP', 'TOTAL_TARIF', 'TARIF_RS',
            'LOS', 'KODE_INACBG', 'SEP'
        ]
        
        # Check required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {
                'is_valid': False,
                'error': f"Missing required columns: {', '.join(missing_columns)}"
            }
        
        # Check for empty required fields
        for col in ['MRN', 'NAMA_PASIEN', 'ADMISSION_DATE']:
            if df[col].isnull().any():
                return {
                    'is_valid': False,
                    'error': f"Column {col} contains null values"
                }
        
        return {'is_valid': True, 'error': None}
    
    def _import_batch(self, batch_df: pd.DataFrame):
        """Import a batch of data to database"""
        try:
            # Import master data first
            self._import_pasien_batch(batch_df)
            self._import_dokter_batch(batch_df)
            self._import_diagnosa_batch(batch_df)
            self._import_prosedur_batch(batch_df)
            
            # Import transaction data
            self._import_kunjungan_batch(batch_df)
            self._import_rincian_biaya_batch(batch_df)
            
            # Import relationship data
            self._import_kunjungan_diagnosa_batch(batch_df)
            self._import_kunjungan_prosedur_batch(batch_df)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            self.import_stats['errors'].append(f"Batch import error: {str(e)}")
    
    def _import_pasien_batch(self, batch_df: pd.DataFrame):
        """Import pasien data"""
        for _, row in batch_df.iterrows():
            try:
                # Check if pasien already exists
                existing_pasien = Pasien.query.filter_by(mrn=row['MRN']).first()
                if existing_pasien:
                    continue
                
                # Create new pasien
                pasien = Pasien(
                    mrn=row['MRN'],
                    nama_pasien=row['NAMA_PASIEN'],
                    birth_date=self._parse_date(row['BIRTH_DATE']),
                    sex=int(row['SEX']) if pd.notna(row['SEX']) else None,
                    no_kartu_bpjs=row.get('NOKARTU'),
                    umur_tahun=int(row['UMUR_TAHUN']) if pd.notna(row.get('UMUR_TAHUN')) else None,
                    umur_hari=int(row['UMUR_HARI']) if pd.notna(row.get('UMUR_HARI')) else None
                )
                
                db.session.add(pasien)
                self.import_stats['imported_pasien'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Pasien import error for MRN {row['MRN']}: {str(e)}")
    
    def _import_dokter_batch(self, batch_df: pd.DataFrame):
        """Import dokter data"""
        for _, row in batch_df.iterrows():
            try:
                if pd.isna(row['DPJP']):
                    continue
                
                # Check if dokter already exists
                existing_dokter = Dokter.query.filter_by(nama_dokter=row['DPJP']).first()
                if existing_dokter:
                    continue
                
                # Create new dokter
                dokter = Dokter(nama_dokter=row['DPJP'])
                db.session.add(dokter)
                self.import_stats['imported_dokter'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Dokter import error for {row['DPJP']}: {str(e)}")
    
    def _import_diagnosa_batch(self, batch_df: pd.DataFrame):
        """Import diagnosa data"""
        for _, row in batch_df.iterrows():
            try:
                if pd.isna(row.get('DIAGLIST')):
                    continue
                
                # Parse diagnosa list
                diagnosa_list = str(row['DIAGLIST']).split(';')
                for diagnosa_code in diagnosa_list:
                    diagnosa_code = diagnosa_code.strip()
                    if not diagnosa_code or diagnosa_code == '-':
                        continue
                    
                    # Check if diagnosa already exists
                    existing_diagnosa = Diagnosa.query.filter_by(kode_diagnosa=diagnosa_code).first()
                    if existing_diagnosa:
                        continue
                    
                    # Create new diagnosa
                    diagnosa = Diagnosa(
                        kode_diagnosa=diagnosa_code,
                        deskripsi=f"Diagnosa {diagnosa_code}"  # Default description
                    )
                    db.session.add(diagnosa)
                    self.import_stats['imported_diagnosa'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Diagnosa import error: {str(e)}")
    
    def _import_prosedur_batch(self, batch_df: pd.DataFrame):
        """Import prosedur data"""
        for _, row in batch_df.iterrows():
            try:
                if pd.isna(row.get('PROCLIST')):
                    continue
                
                # Parse prosedur list
                prosedur_list = str(row['PROCLIST']).split(';')
                for prosedur_code in prosedur_list:
                    prosedur_code = prosedur_code.strip()
                    if not prosedur_code or prosedur_code == '-':
                        continue
                    
                    # Check if prosedur already exists
                    existing_prosedur = Prosedur.query.filter_by(kode_prosedur=prosedur_code).first()
                    if existing_prosedur:
                        continue
                    
                    # Create new prosedur
                    prosedur = Prosedur(
                        kode_prosedur=prosedur_code,
                        deskripsi=f"Prosedur {prosedur_code}"  # Default description
                    )
                    db.session.add(prosedur)
                    self.import_stats['imported_prosedur'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Prosedur import error: {str(e)}")
    
    def _import_kunjungan_batch(self, batch_df: pd.DataFrame):
        """Import kunjungan data"""
        for _, row in batch_df.iterrows():
            try:
                # Get dokter_id
                dokter_id = None
                if pd.notna(row['DPJP']):
                    dokter = Dokter.query.filter_by(nama_dokter=row['DPJP']).first()
                    if dokter:
                        dokter_id = dokter.dokter_id
                
                # Create kunjungan
                kunjungan = Kunjungan(
                    mrn=row['MRN'],
                    dokter_id=dokter_id,
                    admission_date=self._parse_date(row['ADMISSION_DATE']),
                    discharge_date=self._parse_date(row['DISCHARGE_DATE']),
                    los=int(row['LOS']) if pd.notna(row['LOS']) else None,
                    kelas_rawat=int(row['KELAS_RAWAT']) if pd.notna(row['KELAS_RAWAT']) else None,
                    discharge_status=row.get('DISCHARGE_STATUS'),
                    kode_inacbg=row.get('KODE_INACBG'),
                    sep=row.get('SEP'),
                    total_tarif=int(row['TOTAL_TARIF']) if pd.notna(row['TOTAL_TARIF']) else 0,
                    tarif_rs=int(row['TARIF_RS']) if pd.notna(row['TARIF_RS']) else 0
                )
                
                db.session.add(kunjungan)
                db.session.flush()  # Get the ID
                self.import_stats['imported_kunjungan'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Kunjungan import error for MRN {row['MRN']}: {str(e)}")
    
    def _import_rincian_biaya_batch(self, batch_df: pd.DataFrame):
        """Import rincian biaya data"""
        for _, row in batch_df.iterrows():
            try:
                # Get the latest kunjungan for this MRN
                kunjungan = Kunjungan.query.filter_by(mrn=row['MRN']).order_by(Kunjungan.kunjungan_id.desc()).first()
                if not kunjungan:
                    continue
                
                # Create rincian biaya
                rincian_biaya = RincianBiaya(
                    kunjungan_id=kunjungan.kunjungan_id,
                    prosedur_non_bedah=int(row.get('PROSEDUR_NON_BEDAH', 0)) if pd.notna(row.get('PROSEDUR_NON_BEDAH')) else 0,
                    prosedur_bedah=int(row.get('PROSEDUR_BEDAH', 0)) if pd.notna(row.get('PROSEDUR_BEDAH')) else 0,
                    konsultasi=int(row.get('KONSULTASI', 0)) if pd.notna(row.get('KONSULTASI')) else 0,
                    tenaga_ahli=int(row.get('TENAGA_AHLI', 0)) if pd.notna(row.get('TENAGA_AHLI')) else 0,
                    keperawatan=int(row.get('KEPERAWATAN', 0)) if pd.notna(row.get('KEPERAWATAN')) else 0,
                    penunjang=int(row.get('PENUNJANG', 0)) if pd.notna(row.get('PENUNJANG')) else 0,
                    radiologi=int(row.get('RADIOLOGI', 0)) if pd.notna(row.get('RADIOLOGI')) else 0,
                    laboratorium=int(row.get('LABORATORIUM', 0)) if pd.notna(row.get('LABORATORIUM')) else 0,
                    pelayanan_darah=int(row.get('PELAYANAN_DARAH', 0)) if pd.notna(row.get('PELAYANAN_DARAH')) else 0,
                    kamar_akomodasi=int(row.get('KAMAR_AKOMODASI', 0)) if pd.notna(row.get('KAMAR_AKOMODASI')) else 0,
                    obat=int(row.get('OBAT', 0)) if pd.notna(row.get('OBAT')) else 0
                )
                
                db.session.add(rincian_biaya)
                self.import_stats['imported_rincian_biaya'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Rincian biaya import error: {str(e)}")
    
    def _import_kunjungan_diagnosa_batch(self, batch_df: pd.DataFrame):
        """Import kunjungan diagnosa relationships"""
        for _, row in batch_df.iterrows():
            try:
                if pd.isna(row.get('DIAGLIST')):
                    continue
                
                # Get the latest kunjungan for this MRN
                kunjungan = Kunjungan.query.filter_by(mrn=row['MRN']).order_by(Kunjungan.kunjungan_id.desc()).first()
                if not kunjungan:
                    continue
                
                # Parse diagnosa list
                diagnosa_list = str(row['DIAGLIST']).split(';')
                for diagnosa_code in diagnosa_list:
                    diagnosa_code = diagnosa_code.strip()
                    if not diagnosa_code or diagnosa_code == '-':
                        continue
                    
                    # Check if relationship already exists
                    existing = KunjunganDiagnosa.query.filter_by(
                        kunjungan_id=kunjungan.kunjungan_id,
                        kode_diagnosa=diagnosa_code
                    ).first()
                    if existing:
                        continue
                    
                    # Create relationship
                    kunjungan_diagnosa = KunjunganDiagnosa(
                        kunjungan_id=kunjungan.kunjungan_id,
                        kode_diagnosa=diagnosa_code
                    )
                    db.session.add(kunjungan_diagnosa)
                    self.import_stats['imported_kunjungan_diagnosa'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Kunjungan diagnosa import error: {str(e)}")
    
    def _import_kunjungan_prosedur_batch(self, batch_df: pd.DataFrame):
        """Import kunjungan prosedur relationships"""
        for _, row in batch_df.iterrows():
            try:
                if pd.isna(row.get('PROCLIST')):
                    continue
                
                # Get the latest kunjungan for this MRN
                kunjungan = Kunjungan.query.filter_by(mrn=row['MRN']).order_by(Kunjungan.kunjungan_id.desc()).first()
                if not kunjungan:
                    continue
                
                # Parse prosedur list
                prosedur_list = str(row['PROCLIST']).split(';')
                for prosedur_code in prosedur_list:
                    prosedur_code = prosedur_code.strip()
                    if not prosedur_code or prosedur_code == '-':
                        continue
                    
                    # Check if relationship already exists
                    existing = KunjunganProsedur.query.filter_by(
                        kunjungan_id=kunjungan.kunjungan_id,
                        kode_prosedur=prosedur_code
                    ).first()
                    if existing:
                        continue
                    
                    # Create relationship
                    kunjungan_prosedur = KunjunganProsedur(
                        kunjungan_id=kunjungan.kunjungan_id,
                        kode_prosedur=prosedur_code
                    )
                    db.session.add(kunjungan_prosedur)
                    self.import_stats['imported_kunjungan_prosedur'] += 1
                
            except Exception as e:
                self.import_stats['errors'].append(f"Kunjungan prosedur import error: {str(e)}")
    
    def _parse_date(self, date_str) -> Optional[datetime]:
        """Parse date string to datetime object"""
        if pd.isna(date_str):
            return None
        
        try:
            # Try different date formats
            date_formats = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
            for fmt in date_formats:
                try:
                    return datetime.strptime(str(date_str), fmt).date()
                except ValueError:
                    continue
            return None
        except:
            return None
    
    def get_import_stats(self) -> Dict[str, Any]:
        """Get import statistics"""
        return self.import_stats.copy()
    
    def clear_import_stats(self):
        """Clear import statistics"""
        self.import_stats = {
            'total_rows': 0,
            'imported_pasien': 0,
            'imported_dokter': 0,
            'imported_diagnosa': 0,
            'imported_prosedur': 0,
            'imported_kunjungan': 0,
            'imported_rincian_biaya': 0,
            'imported_kunjungan_diagnosa': 0,
            'imported_kunjungan_prosedur': 0,
            'errors': []
        }
