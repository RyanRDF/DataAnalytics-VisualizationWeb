"""
Database Query Service for querying data from database
"""
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy import func, and_, or_

from .database import db, Pasien, Dokter, Diagnosa, Prosedur, Kunjungan, RincianBiaya, KunjunganDiagnosa, KunjunganProsedur


class DatabaseQueryService:
    """Service for querying data from database"""
    
    def __init__(self):
        pass
    
    def get_financial_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get financial data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with financial data
        """
        try:
            # Base query
            query = db.session.query(
                Kunjungan.kunjungan_id,
                Kunjungan.mrn,
                Pasien.nama_pasien,
                Pasien.no_kartu_bpjs,
                Dokter.nama_dokter.label('dpjp'),
                Kunjungan.admission_date,
                Kunjungan.discharge_date,
                Kunjungan.los,
                Kunjungan.kelas_rawat,
                Kunjungan.kode_inacbg,
                Kunjungan.sep,
                Kunjungan.total_tarif,
                Kunjungan.tarif_rs,
                RincianBiaya.prosedur_non_bedah,
                RincianBiaya.prosedur_bedah,
                RincianBiaya.konsultasi,
                RincianBiaya.tenaga_ahli,
                RincianBiaya.keperawatan,
                RincianBiaya.penunjang,
                RincianBiaya.radiologi,
                RincianBiaya.laboratorium,
                RincianBiaya.pelayanan_darah,
                RincianBiaya.kamar_akomodasi,
                RincianBiaya.obat
            ).join(
                Pasien, Kunjungan.mrn == Pasien.mrn
            ).outerjoin(
                Dokter, Kunjungan.dokter_id == Dokter.dokter_id
            ).outerjoin(
                RincianBiaya, Kunjungan.kunjungan_id == RincianBiaya.kunjungan_id
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            # Calculate additional financial metrics
            if not df.empty:
                df['selisih_tarif'] = df['total_tarif'] - df['tarif_rs']
                df['persentase_selisih'] = (df['selisih_tarif'] / df['tarif_rs'] * 100).round(2)
                df['tarif_per_hari'] = (df['total_tarif'] / df['los']).round(2)
            
            return df
            
        except Exception as e:
            print(f"Error querying financial data: {e}")
            return pd.DataFrame()
    
    def get_patient_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get patient data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with patient data
        """
        try:
            # Base query
            query = db.session.query(
                Pasien.mrn,
                Pasien.nama_pasien,
                Pasien.birth_date,
                Pasien.sex,
                Pasien.no_kartu_bpjs,
                Pasien.umur_tahun,
                Pasien.umur_hari,
                func.count(Kunjungan.kunjungan_id).label('jumlah_kunjungan'),
                func.avg(Kunjungan.los).label('rata_los'),
                func.sum(Kunjungan.total_tarif).label('total_biaya')
            ).outerjoin(
                Kunjungan, Pasien.mrn == Kunjungan.mrn
            ).group_by(
                Pasien.mrn, Pasien.nama_pasien, Pasien.birth_date, 
                Pasien.sex, Pasien.no_kartu_bpjs, Pasien.umur_tahun, Pasien.umur_hari
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            return df
            
        except Exception as e:
            print(f"Error querying patient data: {e}")
            return pd.DataFrame()
    
    def get_los_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get Length of Stay data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with LOS data
        """
        try:
            # Base query
            query = db.session.query(
                Kunjungan.kode_inacbg,
                func.count(Kunjungan.kunjungan_id).label('jumlah_kunjungan'),
                func.avg(Kunjungan.los).label('rata_los'),
                func.min(Kunjungan.los).label('min_los'),
                func.max(Kunjungan.los).label('max_los'),
                func.median(Kunjungan.los).label('median_los')
            ).group_by(Kunjungan.kode_inacbg)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            return df
            
        except Exception as e:
            print(f"Error querying LOS data: {e}")
            return pd.DataFrame()
    
    def get_inacbg_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get INA-CBG data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with INA-CBG data
        """
        try:
            # Base query
            query = db.session.query(
                Kunjungan.kode_inacbg,
                func.count(Kunjungan.kunjungan_id).label('jumlah_kunjungan'),
                func.avg(Kunjungan.total_tarif).label('rata_tarif'),
                func.sum(Kunjungan.total_tarif).label('total_tarif'),
                func.avg(Kunjungan.los).label('rata_los')
            ).group_by(Kunjungan.kode_inacbg)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            return df
            
        except Exception as e:
            print(f"Error querying INA-CBG data: {e}")
            return pd.DataFrame()
    
    def get_ventilator_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get ventilator data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with ventilator data
        """
        try:
            # Base query - assuming ventilator data is in a separate table or field
            # For now, return empty DataFrame as placeholder
            query = db.session.query(
                Kunjungan.kunjungan_id,
                Kunjungan.mrn,
                Pasien.nama_pasien,
                Kunjungan.admission_date,
                Kunjungan.discharge_date,
                Kunjungan.los
            ).join(
                Pasien, Kunjungan.mrn == Pasien.mrn
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            return df
            
        except Exception as e:
            print(f"Error querying ventilator data: {e}")
            return pd.DataFrame()
    
    def get_selisih_tarif_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get selisih tarif data from database
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with selisih tarif data
        """
        try:
            # Base query
            query = db.session.query(
                Kunjungan.kunjungan_id,
                Kunjungan.mrn,
                Pasien.nama_pasien,
                Kunjungan.kode_inacbg,
                Kunjungan.total_tarif,
                Kunjungan.tarif_rs,
                (Kunjungan.total_tarif - Kunjungan.tarif_rs).label('selisih_tarif')
            ).join(
                Pasien, Kunjungan.mrn == Pasien.mrn
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            result = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in result])
            
            # Calculate additional metrics
            if not df.empty:
                df['persentase_selisih'] = (df['selisih_tarif'] / df['tarif_rs'] * 100).round(2)
            
            return df
            
        except Exception as e:
            print(f"Error querying selisih tarif data: {e}")
            return pd.DataFrame()
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query"""
        try:
            # Date range filter
            if 'start_date' in filters and filters['start_date']:
                start_date = datetime.strptime(filters['start_date'], '%Y-%m-%d').date()
                query = query.filter(Kunjungan.admission_date >= start_date)
            
            if 'end_date' in filters and filters['end_date']:
                end_date = datetime.strptime(filters['end_date'], '%Y-%m-%d').date()
                query = query.filter(Kunjungan.admission_date <= end_date)
            
            # MRN filter
            if 'mrn' in filters and filters['mrn']:
                query = query.filter(Kunjungan.mrn == filters['mrn'])
            
            # Kode INACBG filter
            if 'kode_inacbg' in filters and filters['kode_inacbg']:
                query = query.filter(Kunjungan.kode_inacbg == filters['kode_inacbg'])
            
            # Kelas rawat filter
            if 'kelas_rawat' in filters and filters['kelas_rawat']:
                query = query.filter(Kunjungan.kelas_rawat == filters['kelas_rawat'])
            
            # Dokter filter
            if 'dokter_id' in filters and filters['dokter_id']:
                query = query.filter(Kunjungan.dokter_id == filters['dokter_id'])
            
            return query
            
        except Exception as e:
            print(f"Error applying filters: {e}")
            return query
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                'total_pasien': Pasien.query.count(),
                'total_dokter': Dokter.query.count(),
                'total_diagnosa': Diagnosa.query.count(),
                'total_prosedur': Prosedur.query.count(),
                'total_kunjungan': Kunjungan.query.count(),
                'total_rincian_biaya': RincianBiaya.query.count(),
                'total_kunjungan_diagnosa': KunjunganDiagnosa.query.count(),
                'total_kunjungan_prosedur': KunjunganProsedur.query.count()
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}
    
    def search_pasien(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for patients by name or MRN"""
        try:
            results = db.session.query(Pasien).filter(
                or_(
                    Pasien.nama_pasien.ilike(f'%{search_term}%'),
                    Pasien.mrn.ilike(f'%{search_term}%')
                )
            ).limit(10).all()
            
            return [pasien.to_dict() for pasien in results]
            
        except Exception as e:
            print(f"Error searching patients: {e}")
            return []
    
    def get_kunjungan_by_pasien(self, mrn: str) -> List[Dict[str, Any]]:
        """Get all kunjungan for a specific patient"""
        try:
            results = db.session.query(Kunjungan).filter(
                Kunjungan.mrn == mrn
            ).order_by(Kunjungan.admission_date.desc()).all()
            
            return [kunjungan.to_dict() for kunjungan in results]
            
        except Exception as e:
            print(f"Error getting kunjungan by patient: {e}")
            return []
