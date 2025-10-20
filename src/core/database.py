"""
Database configuration and models for PostgreSQL
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from utils.timezone_utils import jakarta_now

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
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=jakarta_now)
    updated_at = db.Column(db.DateTime, default=jakarta_now)
    last_login = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    # Relationships
    created_users = db.relationship('User', backref=db.backref('creator', remote_side=[user_id]))
    sessions = db.relationship('UserSession', lazy=True, cascade='all, delete-orphan')
    uploads = db.relationship('UploadLog', lazy=True, cascade='all, delete-orphan')
    login_logs = db.relationship('LoginLog', lazy=True, cascade='all, delete-orphan')
    activity_logs = db.relationship('UserActivityLog', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def create_session(self, ip_address=None, user_agent=None):
        """Create a new session for user"""
        # Clean old sessions
        UserSession.query.filter_by(user_id=self.user_id).filter(
            UserSession.expires_at < jakarta_now()
        ).delete()
        
        # Create new session
        session_token = secrets.token_urlsafe(32)
        session = UserSession(
            user_id=self.user_id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=jakarta_now() + timedelta(hours=24)  # 24 hour session
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
        ).filter(UserSession.expires_at > jakarta_now()).first()
        return session.user if session else None
    
    def log_activity(self, activity_type, description, table_affected=None, record_id=None, 
                    old_values=None, new_values=None, ip_address=None, user_agent=None, session_id=None):
        """Log user activity"""
        activity = UserActivityLog(
            user_id=self.user_id,
            activity_type=activity_type,
            activity_description=description,
            table_affected=table_affected,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id
        )
        db.session.add(activity)
        db.session.commit()
        return activity
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}: {self.email}>'

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(45))  # IPv4/IPv6
    user_agent = db.Column(db.Text)
    login_time = db.Column(db.DateTime, default=jakarta_now)
    logout_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relationship
    user = db.relationship('User')

class UploadLog(db.Model):
    __tablename__ = 'upload_logs'
    
    upload_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.BigInteger)
    file_type = db.Column(db.String(50))
    upload_time = db.Column(db.DateTime, default=jakarta_now)
    status = db.Column(db.String(20), default='processing')  # processing, success, failed, cancelled
    rows_processed = db.Column(db.Integer, default=0)
    rows_success = db.Column(db.Integer, default=0)
    rows_failed = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    processing_time_seconds = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    
    # Relationship
    user = db.relationship('User')
    
    def to_dict(self):
        return {
            'upload_id': self.upload_id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'upload_time': self.upload_time.isoformat() if self.upload_time else None,
            'status': self.status,
            'rows_processed': self.rows_processed,
            'rows_success': self.rows_success,
            'rows_failed': self.rows_failed,
            'error_message': self.error_message,
            'processing_time_seconds': self.processing_time_seconds
        }

class LoginLog(db.Model):
    __tablename__ = 'login_logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    login_time = db.Column(db.DateTime, default=jakarta_now)
    logout_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False)  # success, failed, blocked
    failure_reason = db.Column(db.String(100))
    session_id = db.Column(db.Integer, db.ForeignKey('user_sessions.session_id'))
    
    # Relationship
    user = db.relationship('User')
    session = db.relationship('UserSession')

class DataAnalytics(db.Model):
    """Tabel utama untuk data analytics"""
    __tablename__ = 'data_analytics'
    
    sep = db.Column(db.String(50), primary_key=True)  # Primary key
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)  # User yang pertama kali mengupload row ini
    kode_rs = db.Column(db.Text)
    kelas_rs = db.Column(db.Text)
    kelas_rawat = db.Column(db.Text)
    kode_tarif = db.Column(db.Text)
    ptd = db.Column(db.Integer)
    admission_date = db.Column(db.Text)
    discharge_date = db.Column(db.Text)
    birth_date = db.Column(db.Text)
    birth_weight = db.Column(db.Numeric)
    sex = db.Column(db.Integer)
    discharge_status = db.Column(db.Integer)
    diaglist = db.Column(db.Text)
    proclist = db.Column(db.Text)
    adl1 = db.Column(db.Text)
    adl2 = db.Column(db.Text)
    in_sp = db.Column(db.Text)
    in_sr = db.Column(db.Text)
    in_si = db.Column(db.Text)
    in_sd = db.Column(db.Text)
    inacbg = db.Column(db.Text)
    subacute = db.Column(db.Text)
    chronic = db.Column(db.Text)
    sp = db.Column(db.Text)
    sr = db.Column(db.Text)
    si = db.Column(db.Text)
    sd = db.Column(db.Text)
    deskripsi_inacbg = db.Column(db.Text)
    tarif_inacbg = db.Column(db.BigInteger)
    tarif_subacute = db.Column(db.BigInteger)
    tarif_chronic = db.Column(db.BigInteger)
    deskripsi_sp = db.Column(db.Text)
    tarif_sp = db.Column(db.BigInteger)
    deskripsi_sr = db.Column(db.Text)
    tarif_sr = db.Column(db.BigInteger)
    deskripsi_si = db.Column(db.Text)
    tarif_si = db.Column(db.BigInteger)
    deskripsi_sd = db.Column(db.Text)
    tarif_sd = db.Column(db.BigInteger)
    total_tarif = db.Column(db.BigInteger)
    tarif_rs = db.Column(db.BigInteger)
    tarif_poli_eks = db.Column(db.BigInteger)
    los = db.Column(db.Integer)
    icu_indikator = db.Column(db.Integer)
    icu_los = db.Column(db.Integer)
    vent_hour = db.Column(db.Integer)
    nama_pasien = db.Column(db.Text)
    mrn = db.Column(db.Text)
    umur_tahun = db.Column(db.Integer)
    umur_hari = db.Column(db.Integer)
    dpjp = db.Column(db.Text)
    nokartu = db.Column(db.Text)
    payor_id = db.Column(db.Text)
    coder_id = db.Column(db.Text)
    versi_inacbg = db.Column(db.Text)
    versi_grouper = db.Column(db.Text)
    c1 = db.Column(db.Text)
    c2 = db.Column(db.Text)
    c3 = db.Column(db.Text)
    c4 = db.Column(db.Text)
    prosedur_non_bedah = db.Column(db.BigInteger)
    prosedur_bedah = db.Column(db.BigInteger)
    konsultasi = db.Column(db.BigInteger)
    tenaga_ahli = db.Column(db.BigInteger)
    keperawatan = db.Column(db.BigInteger)
    penunjang = db.Column(db.BigInteger)
    radiologi = db.Column(db.BigInteger)
    laboratorium = db.Column(db.BigInteger)
    pelayanan_darah = db.Column(db.BigInteger)
    rehabilitasi = db.Column(db.BigInteger)
    kamar_akomodasi = db.Column(db.BigInteger)
    rawat_intensif = db.Column(db.BigInteger)
    obat = db.Column(db.BigInteger)
    alkes = db.Column(db.BigInteger)
    bmhp = db.Column(db.BigInteger)
    sewa_alat = db.Column(db.BigInteger)
    obat_kronis = db.Column(db.BigInteger)
    obat_kemo = db.Column(db.BigInteger)
    
    # Relationship
    uploader = db.relationship('User', foreign_keys=[uploader_id])


class UserActivityLog(db.Model):
    __tablename__ = 'user_activity_logs'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    activity_type = db.Column(db.String(50), nullable=False)
    activity_description = db.Column(db.Text)
    table_affected = db.Column(db.String(100))
    record_id = db.Column(db.String(100))
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    activity_time = db.Column(db.DateTime, default=jakarta_now)
    session_id = db.Column(db.Integer, db.ForeignKey('user_sessions.session_id'))
    
    # Relationship
    user = db.relationship('User')
    session = db.relationship('UserSession')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    role_description = db.Column(db.Text)
    permissions = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=jakarta_now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    # Relationship
    creator = db.relationship('User')
    assignments = db.relationship('UserRoleAssignment', lazy=True, cascade='all, delete-orphan')

class UserRoleAssignment(db.Model):
    __tablename__ = 'user_role_assignments'
    
    assignment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.role_id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=jakarta_now)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship
    user = db.relationship('User', foreign_keys=[user_id])
    assigner = db.relationship('User', foreign_keys=[assigned_by])
    role = db.relationship('UserRole')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'role_id', name='unique_user_role'),)
