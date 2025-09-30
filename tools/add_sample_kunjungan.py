#!/usr/bin/env python3
"""
Script untuk menambahkan sample data kunjungan ke database
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.database import db, Pasien, Kunjungan, Dokter, RincianBiaya
from web.app import create_app

def add_sample_kunjungan():
    """Menambahkan sample data kunjungan"""
    
    app = create_app()
    with app.app_context():
        print("🏥 Menambahkan Sample Data Kunjungan...")
        
        # Get existing data
        pasien_list = Pasien.query.all()
        dokter_list = Dokter.query.all()
        
        if not pasien_list:
            print("❌ Tidak ada data pasien!")
            return False
            
        if not dokter_list:
            print("❌ Tidak ada data dokter!")
            return False
        
        # Sample data kunjungan
        sample_kunjungan = [
            {
                'mrn': 'MRN001',
                'dokter_id': 4,  # Dr. Ahmad Wijaya
                'admission_date': '2024-01-15',
                'discharge_date': '2024-01-20',
                'los': 5,
                'kelas_rawat': 2,
                'kode_inacbg': 'A001',
                'total_tarif': 5000000,
                'tarif_rs': 4500000,
                'sep': 'SEP001',
                'discharge_status': 'Sembuh'
            },
            {
                'mrn': 'MRN002',
                'dokter_id': 5,  # Dr. Siti Nurhaliza
                'admission_date': '2024-01-20',
                'discharge_date': '2024-01-25',
                'los': 5,
                'kelas_rawat': 1,
                'kode_inacbg': 'A002',
                'total_tarif': 7500000,
                'tarif_rs': 7000000,
                'sep': 'SEP002',
                'discharge_status': 'Sembuh'
            },
            {
                'mrn': 'MRN003',
                'dokter_id': 6,  # Dr. Budi Santoso
                'admission_date': '2024-02-01',
                'discharge_date': '2024-02-08',
                'los': 7,
                'kelas_rawat': 3,
                'kode_inacbg': 'A003',
                'total_tarif': 12000000,
                'tarif_rs': 11000000,
                'sep': 'SEP003',
                'discharge_status': 'Sembuh'
            },
            {
                'mrn': 'MRN001',
                'dokter_id': 4,  # Dr. Ahmad Wijaya
                'admission_date': '2024-02-15',
                'discharge_date': '2024-02-18',
                'los': 3,
                'kelas_rawat': 2,
                'kode_inacbg': 'A004',
                'total_tarif': 3500000,
                'tarif_rs': 3200000,
                'sep': 'SEP004',
                'discharge_status': 'Sembuh'
            },
            {
                'mrn': 'MRN002',
                'dokter_id': 5,  # Dr. Siti Nurhaliza
                'admission_date': '2024-03-01',
                'discharge_date': '2024-03-06',
                'los': 5,
                'kelas_rawat': 1,
                'kode_inacbg': 'A005',
                'total_tarif': 8000000,
                'tarif_rs': 7500000,
                'sep': 'SEP005',
                'discharge_status': 'Sembuh'
            }
        ]
        
        # Sample rincian biaya
        sample_rincian = [
            {
                'prosedur_non_bedah': 1000000,
                'prosedur_bedah': 2000000,
                'konsultasi': 500000,
                'obat': 1500000
            },
            {
                'prosedur_non_bedah': 1500000,
                'prosedur_bedah': 3000000,
                'konsultasi': 750000,
                'obat': 2250000
            },
            {
                'prosedur_non_bedah': 2000000,
                'prosedur_bedah': 5000000,
                'konsultasi': 1000000,
                'obat': 4000000
            },
            {
                'prosedur_non_bedah': 800000,
                'prosedur_bedah': 1500000,
                'konsultasi': 400000,
                'obat': 800000
            },
            {
                'prosedur_non_bedah': 1800000,
                'prosedur_bedah': 3500000,
                'konsultasi': 900000,
                'obat': 1800000
            }
        ]
        
        try:
            # Insert kunjungan data
            for i, kunjungan_data in enumerate(sample_kunjungan):
                kunjungan = Kunjungan(**kunjungan_data)
                db.session.add(kunjungan)
                db.session.flush()  # Get the ID
                
                # Add rincian biaya
                rincian_data = sample_rincian[i]
                rincian_data['kunjungan_id'] = kunjungan.kunjungan_id
                rincian = RincianBiaya(**rincian_data)
                db.session.add(rincian)
            
            db.session.commit()
            
            # Verify data
            kunjungan_count = Kunjungan.query.count()
            rincian_count = RincianBiaya.query.count()
            
            print(f"✅ Sample data berhasil ditambahkan!")
            print(f"   - Kunjungan: {kunjungan_count} records")
            print(f"   - Rincian Biaya: {rincian_count} records")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 ADD SAMPLE KUNJUNGAN DATA")
    print("=" * 60)
    
    success = add_sample_kunjungan()
    
    if success:
        print("\n🎉 Sample data kunjungan berhasil ditambahkan!")
        print("📊 Sekarang Anda dapat melihat analisis di aplikasi web.")
    else:
        print("\n❌ Gagal menambahkan sample data.")
    
    print("=" * 60)
