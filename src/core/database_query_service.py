"""
Database Query Service for querying data from database
Simplified version focusing only on DataAnalytics table
"""
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy import func, and_, or_

from core.database import db, DataAnalytics


class DatabaseQueryService:
    """Service for querying data from database - simplified for DataAnalytics only"""
    
    def __init__(self):
        pass
    
    def get_financial_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get financial data from DataAnalytics table
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with financial data
        """
        try:
            # Base query using DataAnalytics table
            query = db.session.query(DataAnalytics)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'sep': row.sep,
                'mrn': row.mrn,
                'nama_pasien': row.nama_pasien,
                'dpjp': row.dpjp,
                'admission_date': row.admission_date,
                'discharge_date': row.discharge_date,
                'los': row.los,
                'kelas_rawat': row.kelas_rawat,
                'inacbg': row.inacbg,
                'total_tarif': row.total_tarif,
                'tarif_rs': row.tarif_rs,
                'prosedur_non_bedah': row.prosedur_non_bedah,
                'prosedur_bedah': row.prosedur_bedah,
                'konsultasi': row.konsultasi,
                'tenaga_ahli': row.tenaga_ahli,
                'keperawatan': row.keperawatan,
                'penunjang': row.penunjang,
                'radiologi': row.radiologi,
                'laboratorium': row.laboratorium,
                'pelayanan_darah': row.pelayanan_darah,
                'kamar_akomodasi': row.kamar_akomodasi,
                'obat': row.obat
            } for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting financial data: {e}")
            return pd.DataFrame()
    
    def get_inacbg_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get INACBG analysis data
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with INACBG data
        """
        try:
            # Base query
            query = db.session.query(
                DataAnalytics.inacbg,
                func.count(DataAnalytics.sep).label('jumlah_kunjungan'),
                func.avg(DataAnalytics.los).label('rata_los'),
                func.min(DataAnalytics.los).label('min_los'),
                func.max(DataAnalytics.los).label('max_los'),
                func.avg(DataAnalytics.total_tarif).label('rata_tarif'),
                func.sum(DataAnalytics.total_tarif).label('total_tarif')
            ).group_by(DataAnalytics.inacbg)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting INACBG data: {e}")
            return pd.DataFrame()
    
    def get_los_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get Length of Stay analysis data
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with LOS data
        """
        try:
            # Base query
            query = db.session.query(
                DataAnalytics.inacbg,
                func.count(DataAnalytics.sep).label('jumlah_kunjungan'),
                func.avg(DataAnalytics.los).label('rata_los'),
                func.min(DataAnalytics.los).label('min_los'),
                func.max(DataAnalytics.los).label('max_los'),
                func.median(DataAnalytics.los).label('median_los')
            ).group_by(DataAnalytics.inacbg)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting LOS data: {e}")
            return pd.DataFrame()
    
    def get_ventilator_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get ventilator usage data
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with ventilator data
        """
        try:
            # Base query
            query = db.session.query(
                DataAnalytics.sep,
                DataAnalytics.mrn,
                DataAnalytics.nama_pasien,
                DataAnalytics.admission_date,
                DataAnalytics.discharge_date,
                DataAnalytics.los,
                DataAnalytics.vent_hour,
                DataAnalytics.icu_indikator,
                DataAnalytics.icu_los
            ).filter(DataAnalytics.vent_hour > 0)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting ventilator data: {e}")
            return pd.DataFrame()
    
    def get_patient_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get patient data
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with patient data
        """
        try:
            # Base query
            query = db.session.query(
                DataAnalytics.sep,
                DataAnalytics.mrn,
                DataAnalytics.nama_pasien,
                DataAnalytics.admission_date,
                DataAnalytics.discharge_date,
                DataAnalytics.los
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting patient data: {e}")
            return pd.DataFrame()
    
    def get_tarif_selisih_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Get tariff difference analysis data
        
        Args:
            filters: Dictionary of filters to apply
            
        Returns:
            DataFrame with tariff difference data
        """
        try:
            # Base query
            query = db.session.query(
                DataAnalytics.sep,
                DataAnalytics.mrn,
                DataAnalytics.nama_pasien,
                DataAnalytics.inacbg,
                DataAnalytics.total_tarif,
                DataAnalytics.tarif_rs,
                (DataAnalytics.total_tarif - DataAnalytics.tarif_rs).label('selisih_tarif')
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting tariff difference data: {e}")
            return pd.DataFrame()
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query"""
        try:
            # Date range filter
            if 'start_date' in filters and filters['start_date']:
                start_date = datetime.strptime(filters['start_date'], '%Y-%m-%d').date()
                query = query.filter(DataAnalytics.admission_date >= start_date)
            
            if 'end_date' in filters and filters['end_date']:
                end_date = datetime.strptime(filters['end_date'], '%Y-%m-%d').date()
                query = query.filter(DataAnalytics.admission_date <= end_date)
            
            # MRN filter
            if 'mrn' in filters and filters['mrn']:
                query = query.filter(DataAnalytics.mrn == filters['mrn'])
            
            # INACBG filter
            if 'kode_inacbg' in filters and filters['kode_inacbg']:
                query = query.filter(DataAnalytics.inacbg == filters['kode_inacbg'])
            
            # Kelas rawat filter
            if 'kelas_rawat' in filters and filters['kelas_rawat']:
                query = query.filter(DataAnalytics.kelas_rawat == filters['kelas_rawat'])
            
            return query
            
        except Exception as e:
            print(f"Error applying filters: {e}")
            return query
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            from core.database import DataAnalytics
            
            stats = {
                'total_data_analytics': DataAnalytics.query.count()
            }
            
            # Calculate total rows (mainly from data_analytics as it's the main table)
            stats['total_rows'] = stats['total_data_analytics']
            
            return stats
            
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}
    
    def search_pasien(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for patients by name or MRN"""
        try:
            results = db.session.query(DataAnalytics).filter(
                or_(
                    DataAnalytics.nama_pasien.ilike(f'%{search_term}%'),
                    DataAnalytics.mrn.ilike(f'%{search_term}%')
                )
            ).limit(10).all()
            
            return [{
                'mrn': row.mrn,
                'nama_pasien': row.nama_pasien,
                'sep': row.sep,
                'admission_date': row.admission_date
            } for row in results]
            
        except Exception as e:
            print(f"Error searching patients: {e}")
            return []
    
    def get_kunjungan_by_pasien(self, mrn: str) -> List[Dict[str, Any]]:
        """Get all kunjungan for a specific patient"""
        try:
            results = db.session.query(DataAnalytics).filter(
                DataAnalytics.mrn == mrn
            ).order_by(DataAnalytics.admission_date.desc()).all()
            
            return [{
                'sep': row.sep,
                'mrn': row.mrn,
                'nama_pasien': row.nama_pasien,
                'admission_date': row.admission_date,
                'discharge_date': row.discharge_date,
                'los': row.los,
                'inacbg': row.inacbg,
                'total_tarif': row.total_tarif
            } for row in results]
            
        except Exception as e:
            print(f"Error getting kunjungan by patient: {e}")
            return []

