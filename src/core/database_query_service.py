"""
Database Query Service for querying data from database
Simplified version focusing only on DataAnalytics table
"""
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

from core.database import db, DataAnalytics


class DatabaseQueryService:
    """Service for querying data from database - simplified for DataAnalytics only"""
    
    def __init__(self):
        pass
    
    def get_financial_data(self, filters: Dict[str, Any] = None, limit: int = 1000) -> pd.DataFrame:
        """
        Get financial data from DataAnalytics table with performance optimization
        
        Args:
            filters: Dictionary of filters to apply
            limit: Maximum number of records to return (default: 1000)
            
        Returns:
            DataFrame with financial data
        """
        try:
            # Base query using DataAnalytics table
            query = db.session.query(DataAnalytics)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Apply limit for performance
            query = query.limit(limit)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'DPJP': row.dpjp,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'LOS': row.los,
                'KELAS_RAWAT': row.kelas_rawat,
                'INACBG': row.inacbg,
                'TOTAL_TARIF': row.total_tarif,
                'TARIF_RS': row.tarif_rs,
                'PROSEDUR_NON_BEDAH': row.prosedur_non_bedah,
                'PROSEDUR_BEDAH': row.prosedur_bedah,
                'KONSULTASI': row.konsultasi,
                'TENAGA_AHLI': row.tenaga_ahli,
                'KEPERAWATAN': row.keperawatan,
                'PENUNJANG': row.penunjang,
                'RADIOLOGI': row.radiologi,
                'LABORATORIUM': row.laboratorium,
                'PELAYANAN_DARAH': row.pelayanan_darah,
                'KAMAR_AKOMODASI': row.kamar_akomodasi,
                'OBAT': row.obat
            } for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting financial data: {e}")
            return pd.DataFrame()
    
    def get_financial_data_paginated(self, filters: Dict[str, Any] = None, 
                                    page: int = 1, per_page: int = 100) -> Dict[str, Any]:
        """
        Get financial data with pagination for better performance
        
        Args:
            filters: Dictionary of filters to apply
            page: Page number (1-based)
            per_page: Number of records per page
            
        Returns:
            Dictionary with data, pagination info, and metadata
        """
        try:
            # Base query using DataAnalytics table
            query = db.session.query(DataAnalytics)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * per_page
            results = query.offset(offset).limit(per_page).all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'DPJP': row.dpjp,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'LOS': row.los,
                'KELAS_RAWAT': row.kelas_rawat,
                'INACBG': row.inacbg,
                'TOTAL_TARIF': row.total_tarif,
                'TARIF_RS': row.tarif_rs,
                'PROSEDUR_NON_BEDAH': row.prosedur_non_bedah,
                'PROSEDUR_BEDAH': row.prosedur_bedah,
                'KONSULTASI': row.konsultasi,
                'TENAGA_AHLI': row.tenaga_ahli,
                'KEPERAWATAN': row.keperawatan,
                'PENUNJANG': row.penunjang,
                'RADIOLOGI': row.radiologi,
                'LABORATORIUM': row.laboratorium,
                'PELAYANAN_DARAH': row.pelayanan_darah,
                'KAMAR_AKOMODASI': row.kamar_akomodasi,
                'OBAT': row.obat
            } for row in results])
            
            return {
                'data': df,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page,
                'has_next': page < (total + per_page - 1) // per_page,
                'has_prev': page > 1
            }
            
        except Exception as e:
            print(f"Error getting paginated financial data: {e}")
            return {
                'data': pd.DataFrame(),
                'total': 0,
                'page': 1,
                'per_page': per_page,
                'pages': 0,
                'has_next': False,
                'has_prev': False,
                'error': str(e)
            }
    
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
                DataAnalytics.deskripsi_inacbg,
                func.count(DataAnalytics.sep).label('jumlah_kunjungan'),
                func.avg(DataAnalytics.los).label('rata_los'),
                func.min(DataAnalytics.los).label('min_los'),
                func.max(DataAnalytics.los).label('max_los'),
                func.avg(DataAnalytics.total_tarif).label('rata_tarif'),
                func.sum(DataAnalytics.total_tarif).label('total_tarif'),
                func.avg(DataAnalytics.tarif_rs).label('rata_tarif_rs'),
                func.sum(DataAnalytics.tarif_rs).label('total_tarif_rs')
            ).group_by(DataAnalytics.inacbg, DataAnalytics.deskripsi_inacbg)
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'INACBG': row.inacbg,
                'DESKRIPSI_INACBG': row.deskripsi_inacbg,
                'jumlah_kunjungan': row.jumlah_kunjungan,
                'rata_los': row.rata_los,
                'min_los': row.min_los,
                'max_los': row.max_los,
                'rata_tarif': row.rata_tarif,
                'total_tarif': row.total_tarif,
                'rata_tarif_rs': row.rata_tarif_rs,
                'total_tarif_rs': row.total_tarif_rs
            } for row in results])
            
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
                DataAnalytics.sep,
                DataAnalytics.mrn,
                DataAnalytics.nama_pasien,
                DataAnalytics.inacbg,
                DataAnalytics.deskripsi_inacbg,
                DataAnalytics.los,
                DataAnalytics.admission_date,
                DataAnalytics.discharge_date,
                DataAnalytics.total_tarif,
                DataAnalytics.tarif_rs
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'INACBG': row.inacbg,
                'DESKRIPSI_INACBG': row.deskripsi_inacbg,
                'LOS': row.los,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'TOTAL_TARIF': row.total_tarif,
                'TARIF_RS': row.tarif_rs
            } for row in results])
            
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
            # Base query - ambil semua data ventilator (termasuk yang tidak menggunakan ventilator)
            query = db.session.query(
                DataAnalytics.sep,
                DataAnalytics.mrn,
                DataAnalytics.nama_pasien,
                DataAnalytics.admission_date,
                DataAnalytics.discharge_date,
                DataAnalytics.los,
                DataAnalytics.vent_hour,
                DataAnalytics.icu_indikator,
                DataAnalytics.icu_los,
                DataAnalytics.inacbg,
                DataAnalytics.deskripsi_inacbg,
                DataAnalytics.total_tarif,
                DataAnalytics.tarif_rs
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'LOS': row.los,
                'VENT_HOUR': row.vent_hour,
                'ICU_INDIKATOR': row.icu_indikator,
                'ICU_LOS': row.icu_los,
                'INACBG': row.inacbg,
                'DESKRIPSI_INACBG': row.deskripsi_inacbg,
                'TOTAL_TARIF': row.total_tarif,
                'TARIF_RS': row.tarif_rs
            } for row in results])
            
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
                DataAnalytics.los,
                DataAnalytics.kelas_rawat,
                DataAnalytics.inacbg,
                DataAnalytics.birth_date,
                DataAnalytics.birth_weight,
                DataAnalytics.sex,
                DataAnalytics.discharge_status,
                DataAnalytics.diaglist,
                DataAnalytics.proclist,
                DataAnalytics.adl1,
                DataAnalytics.adl2,
                DataAnalytics.umur_tahun,
                DataAnalytics.umur_hari,
                DataAnalytics.dpjp,
                DataAnalytics.nokartu,
                DataAnalytics.payor_id,
                DataAnalytics.coder_id,
                DataAnalytics.versi_inacbg,
                DataAnalytics.versi_grouper
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'LOS': row.los,
                'KELAS_RAWAT': row.kelas_rawat,
                'INACBG': row.inacbg,
                'BIRTH_DATE': row.birth_date,
                'BIRTH_WEIGHT': row.birth_weight,
                'SEX': row.sex,
                'DISCHARGE_STATUS': row.discharge_status,
                'DIAGLIST': row.diaglist,
                'PROCLIST': row.proclist,
                'ADL1': row.adl1,
                'ADL2': row.adl2,
                'UMUR_TAHUN': row.umur_tahun,
                'UMUR_HARI': row.umur_hari,
                'DPJP': row.dpjp,
                'NOKARTU': row.nokartu,
                'PAYOR_ID': row.payor_id,
                'CODER_ID': row.coder_id,
                'VERSI_INACBG': row.versi_inacbg,
                'VERSI_GROUPER': row.versi_grouper
            } for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting patient data: {e}")
            return pd.DataFrame()
    
    def get_selisih_tarif_data(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
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
                DataAnalytics.los,
                DataAnalytics.diaglist,
                DataAnalytics.proclist,
                DataAnalytics.admission_date,
                DataAnalytics.discharge_date,
                (DataAnalytics.total_tarif - DataAnalytics.tarif_rs).label('SELISIH_TARIF')
            )
            
            # Apply filters
            if filters:
                query = self._apply_filters(query, filters)
            
            # Execute query
            results = query.all()
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'SEP': row.sep,
                'MRN': row.mrn,
                'NAMA_PASIEN': row.nama_pasien,
                'INACBG': row.inacbg,
                'TOTAL_TARIF': row.total_tarif,
                'TARIF_RS': row.tarif_rs,
                'LOS': row.los,
                'DIAGLIST': row.diaglist,
                'PROCLIST': row.proclist,
                'ADMISSION_DATE': row.admission_date,
                'DISCHARGE_DATE': row.discharge_date,
                'SELISIH_TARIF': row.SELISIH_TARIF
            } for row in results])
            
            return df
            
        except Exception as e:
            print(f"Error getting tariff difference data: {e}")
            return pd.DataFrame()
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query with flexible filtering"""
        try:
            # Helper: parse a date string to format yang sesuai dengan database (YYYY-MM-DD HH:MM:SS)
            def _parse_date_str(s: str):
                if not s:
                    return None
                s = str(s).strip()
                # Try common formats dan return string dalam format database
                date_formats = [
                    '%Y-%m-%d',           # YYYY-MM-DD
                    '%d/%m/%Y',           # DD/MM/YYYY
                    '%Y/%m/%d',           # YYYY/MM/DD
                    '%d-%m-%Y',           # DD-MM-YYYY
                    '%Y-%m-%d %H:%M:%S'   # YYYY-MM-DD HH:MM:SS
                ]
                
                for fmt in date_formats:
                    try:
                        # Parse ke datetime object
                        dt = datetime.strptime(s, fmt)
                        # Return string dengan format yang sesuai database (YYYY-MM-DD HH:MM:SS)
                        return dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        continue
                
                # Try pandas as a last resort (handles ISO and other variants)
                try:
                    dt = pd.to_datetime(s, errors='coerce')
                    if pd.isna(dt):
                        return None
                    # Return string dengan format yang sesuai database
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    return None

            # Date range filter - menggunakan string comparison karena admission_date adalah TEXT
            if 'start_date' in filters and filters['start_date']:
                # Parse start date ke format database (YYYY-MM-DD 00:00:00)
                start_date_str = _parse_date_str(filters['start_date'])
                if start_date_str:
                    # Set jam ke 00:00:00 untuk awal hari
                    if len(start_date_str) == 10:  # Hanya tanggal tanpa waktu
                        start_date_str = start_date_str + ' 00:00:00'
                    query = query.filter(DataAnalytics.admission_date >= start_date_str)

            if 'end_date' in filters and filters['end_date']:
                # Parse end date ke format database dan set ke akhir hari (23:59:59)
                end_date_str = _parse_date_str(filters['end_date'])
                if end_date_str:
                    # Set jam ke 23:59:59 untuk akhir hari
                    if len(end_date_str) == 10:  # Hanya tanggal tanpa waktu
                        end_date_str = end_date_str + ' 23:59:59'
                    else:
                        # Jika sudah ada waktu, ganti dengan 23:59:59
                        end_date_str = end_date_str.split()[0] + ' 23:59:59'
                    query = query.filter(DataAnalytics.admission_date <= end_date_str)
            
            # Specific column filter (flexible)
            if 'filter_column' in filters and 'filter_value' in filters:
                filter_column = filters['filter_column']
                filter_value = filters['filter_value']
                
                if filter_column and filter_value:
                    # Get the column attribute dynamically
                    if hasattr(DataAnalytics, filter_column):
                        column_attr = getattr(DataAnalytics, filter_column)
                        # Use case-insensitive search for text columns
                        if column_attr.type.python_type == str:
                            query = query.filter(column_attr.ilike(f'%{filter_value}%'))
                        else:
                            # For non-string columns, try exact match first, then convert to string for partial match
                            try:
                                query = query.filter(column_attr == filter_value)
                            except:
                                query = query.filter(column_attr.cast(db.String).ilike(f'%{filter_value}%'))
            
            # Legacy filters for backward compatibility
            if 'mrn' in filters and filters['mrn']:
                query = query.filter(DataAnalytics.mrn.ilike(f'%{filters["mrn"]}%'))
            
            if 'kode_inacbg' in filters and filters['kode_inacbg']:
                query = query.filter(DataAnalytics.inacbg.ilike(f'%{filters["kode_inacbg"]}%'))
            
            if 'kelas_rawat' in filters and filters['kelas_rawat']:
                query = query.filter(DataAnalytics.kelas_rawat.ilike(f'%{filters["kelas_rawat"]}%'))
            
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

