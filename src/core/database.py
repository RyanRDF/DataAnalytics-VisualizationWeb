"""
Database configuration and models for PostgreSQL
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with Flask app"""
    
    # Database configuration - langsung hardcode sesuai permintaan
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'DAV'
    DB_USER = 'postgres'
    DB_PASSWORD = 'admin'
    
    # PostgreSQL connection string
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def create_session(self):
        """Create a new session for user"""
        # Clean old sessions
        UserSession.query.filter_by(user_id=self.id).filter(
            UserSession.expires_at < datetime.utcnow()
        ).delete()
        
        # Create new session
        session_token = secrets.token_urlsafe(32)
        session = UserSession(
            user_id=self.id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)  # 24 hour session
        )
        db.session.add(session)
        db.session.commit()
        
        return session_token
    
    @staticmethod
    def get_by_session_token(token):
        """Get user by session token"""
        session = UserSession.query.filter_by(
            session_token=token,
            is_active=True
        ).filter(UserSession.expires_at > datetime.utcnow()).first()
        return session.user if session else None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))

class DataUploadLog(db.Model):
    __tablename__ = 'data_upload_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    rows_processed = db.Column(db.Integer)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='success')  # success, error, processing
    error_message = db.Column(db.Text)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('uploads', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_size': self.file_size,
            'rows_processed': self.rows_processed,
            'upload_time': self.upload_time.isoformat() if self.upload_time else None,
            'status': self.status,
            'error_message': self.error_message
        }

# =============================================
# HOSPITAL DATABASE MODELS
# =============================================

class Pasien(db.Model):
    """Tabel untuk menyimpan data unik pasien"""
    __tablename__ = 'pasien'
    
    mrn = db.Column(db.String(20), primary_key=True)  # Medical Record Number
    nama_pasien = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date)
    sex = db.Column(db.SmallInteger)  # 1 Laki-laki, 2 Perempuan
    no_kartu_bpjs = db.Column(db.String(20), unique=True)
    umur_tahun = db.Column(db.Integer)
    umur_hari = db.Column(db.Integer)
    
    # Relationships
    kunjungan = db.relationship('Kunjungan', backref='pasien', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'mrn': self.mrn,
            'nama_pasien': self.nama_pasien,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'sex': self.sex,
            'no_kartu_bpjs': self.no_kartu_bpjs,
            'umur_tahun': self.umur_tahun,
            'umur_hari': self.umur_hari
        }
    
    def __repr__(self):
        return f'<Pasien {self.mrn}: {self.nama_pasien}>'

class Dokter(db.Model):
    """Tabel untuk menyimpan data dokter"""
    __tablename__ = 'dokter'
    
    dokter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_dokter = db.Column(db.String(255), nullable=False)
    
    # Relationships
    kunjungan = db.relationship('Kunjungan', backref='dokter', lazy=True)
    
    def to_dict(self):
        return {
            'dokter_id': self.dokter_id,
            'nama_dokter': self.nama_dokter
        }
    
    def __repr__(self):
        return f'<Dokter {self.dokter_id}: {self.nama_dokter}>'

class Diagnosa(db.Model):
    """Tabel lookup untuk kode diagnosa (ICD-10)"""
    __tablename__ = 'diagnosa'
    
    kode_diagnosa = db.Column(db.String(10), primary_key=True)
    deskripsi = db.Column(db.Text, nullable=False)
    
    # Relationships
    kunjungan_diagnosa = db.relationship('KunjunganDiagnosa', backref='diagnosa', lazy=True)
    
    def to_dict(self):
        return {
            'kode_diagnosa': self.kode_diagnosa,
            'deskripsi': self.deskripsi
        }
    
    def __repr__(self):
        return f'<Diagnosa {self.kode_diagnosa}: {self.deskripsi[:50]}...>'

class Prosedur(db.Model):
    """Tabel lookup untuk kode prosedur medis (ICD-9CM)"""
    __tablename__ = 'prosedur'
    
    kode_prosedur = db.Column(db.String(10), primary_key=True)
    deskripsi = db.Column(db.Text, nullable=False)
    
    # Relationships
    kunjungan_prosedur = db.relationship('KunjunganProsedur', backref='prosedur', lazy=True)
    
    def to_dict(self):
        return {
            'kode_prosedur': self.kode_prosedur,
            'deskripsi': self.deskripsi
        }
    
    def __repr__(self):
        return f'<Prosedur {self.kode_prosedur}: {self.deskripsi[:50]}...>'

class Kunjungan(db.Model):
    """Tabel utama untuk mencatat setiap kunjungan/rawat inap pasien"""
    __tablename__ = 'kunjungan'
    
    kunjungan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mrn = db.Column(db.String(20), db.ForeignKey('pasien.mrn'), nullable=False)
    dokter_id = db.Column(db.Integer, db.ForeignKey('dokter.dokter_id'))
    admission_date = db.Column(db.Date, nullable=False)
    discharge_date = db.Column(db.Date)
    los = db.Column(db.Integer)  # Length of Stay (dalam hari)
    kelas_rawat = db.Column(db.SmallInteger)  # Kode kelas rawat (1, 2, 3)
    discharge_status = db.Column(db.String(50))
    kode_inacbg = db.Column(db.String(20))
    sep = db.Column(db.String(50))  # Nomor Surat Eligibilitas Peserta
    total_tarif = db.Column(db.BigInteger, default=0)
    tarif_rs = db.Column(db.BigInteger, default=0)
    
    # Relationships
    rincian_biaya = db.relationship('RincianBiaya', backref='kunjungan', lazy=True, uselist=False, cascade='all, delete-orphan')
    kunjungan_diagnosa = db.relationship('KunjunganDiagnosa', backref='kunjungan', lazy=True, cascade='all, delete-orphan')
    kunjungan_prosedur = db.relationship('KunjunganProsedur', backref='kunjungan', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'kunjungan_id': self.kunjungan_id,
            'mrn': self.mrn,
            'dokter_id': self.dokter_id,
            'admission_date': self.admission_date.isoformat() if self.admission_date else None,
            'discharge_date': self.discharge_date.isoformat() if self.discharge_date else None,
            'los': self.los,
            'kelas_rawat': self.kelas_rawat,
            'discharge_status': self.discharge_status,
            'kode_inacbg': self.kode_inacbg,
            'sep': self.sep,
            'total_tarif': self.total_tarif,
            'tarif_rs': self.tarif_rs
        }
    
    def __repr__(self):
        return f'<Kunjungan {self.kunjungan_id}: {self.mrn} - {self.admission_date}>'

class RincianBiaya(db.Model):
    """Tabel untuk rincian biaya, relasi One-to-One dengan Kunjungan"""
    __tablename__ = 'rincian_biaya'
    
    rincian_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kunjungan_id = db.Column(db.Integer, db.ForeignKey('kunjungan.kunjungan_id'), nullable=False, unique=True)
    prosedur_non_bedah = db.Column(db.BigInteger, default=0)
    prosedur_bedah = db.Column(db.BigInteger, default=0)
    konsultasi = db.Column(db.BigInteger, default=0)
    tenaga_ahli = db.Column(db.BigInteger, default=0)
    keperawatan = db.Column(db.BigInteger, default=0)
    penunjang = db.Column(db.BigInteger, default=0)
    radiologi = db.Column(db.BigInteger, default=0)
    laboratorium = db.Column(db.BigInteger, default=0)
    pelayanan_darah = db.Column(db.BigInteger, default=0)
    kamar_akomodasi = db.Column(db.BigInteger, default=0)
    obat = db.Column(db.BigInteger, default=0)
    
    def to_dict(self):
        return {
            'rincian_id': self.rincian_id,
            'kunjungan_id': self.kunjungan_id,
            'prosedur_non_bedah': self.prosedur_non_bedah,
            'prosedur_bedah': self.prosedur_bedah,
            'konsultasi': self.konsultasi,
            'tenaga_ahli': self.tenaga_ahli,
            'keperawatan': self.keperawatan,
            'penunjang': self.penunjang,
            'radiologi': self.radiologi,
            'laboratorium': self.laboratorium,
            'pelayanan_darah': self.pelayanan_darah,
            'kamar_akomodasi': self.kamar_akomodasi,
            'obat': self.obat
        }
    
    def __repr__(self):
        return f'<RincianBiaya {self.rincian_id}: Kunjungan {self.kunjungan_id}>'

class KunjunganDiagnosa(db.Model):
    """Menghubungkan Kunjungan dengan banyak Diagnosa (Many-to-Many)"""
    __tablename__ = 'kunjungan_diagnosa'
    
    kunjungan_id = db.Column(db.Integer, db.ForeignKey('kunjungan.kunjungan_id'), primary_key=True)
    kode_diagnosa = db.Column(db.String(10), db.ForeignKey('diagnosa.kode_diagnosa'), primary_key=True)
    
    def to_dict(self):
        return {
            'kunjungan_id': self.kunjungan_id,
            'kode_diagnosa': self.kode_diagnosa
        }
    
    def __repr__(self):
        return f'<KunjunganDiagnosa {self.kunjungan_id} - {self.kode_diagnosa}>'

class KunjunganProsedur(db.Model):
    """Menghubungkan Kunjungan dengan banyak Prosedur (Many-to-Many)"""
    __tablename__ = 'kunjungan_prosedur'
    
    kunjungan_id = db.Column(db.Integer, db.ForeignKey('kunjungan.kunjungan_id'), primary_key=True)
    kode_prosedur = db.Column(db.String(10), db.ForeignKey('prosedur.kode_prosedur'), primary_key=True)
    
    def to_dict(self):
        return {
            'kunjungan_id': self.kunjungan_id,
            'kode_prosedur': self.kode_prosedur
        }
    
    def __repr__(self):
        return f'<KunjunganProsedur {self.kunjungan_id} - {self.kode_prosedur}>'