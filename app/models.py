from app import db
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    sex = db.Column(db.String(10))  # 'Male' or 'Female'
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', backref='client', lazy=True)
    lab_results = db.relationship('LabResult', backref='client', lazy=True)
    hhq_responses = db.relationship('HHQResponse', back_populates='client', lazy='dynamic')

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

class LabResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    test_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    reference_range = db.Column(db.String(50))
    date_collected = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lab_results = db.relationship('LabResult', backref='report', lazy=True)
    hhq_data = db.Column(db.JSON)
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')

class HHQResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    unique_token = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    responses = db.Column(db.JSON, nullable=False, default=dict)
    status = db.Column(db.String(20), default='sent')  # sent, viewed, in_progress, completed
    expires_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=30))
    last_modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # Supports IPv6 addresses
    user_agent = db.Column(db.String(255), nullable=True)
    
    client = db.relationship('Client', back_populates='hhq_responses')

    __table_args__ = (
        db.UniqueConstraint('unique_token', name='uq_hhq_response_token'),
    )

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def progress_percentage(self):
        if not self.responses:
            return 0
            
        # Define total questions per section (excluding pre-screening)
        section_questions = {
            0: 13,  # Dementia Prevention
            1: 13,  # Has a Diagnosis of Dementia
            2: 1,   # Family History
            3: 12,  # Head Trauma
            4: 14,  # History of Headaches
            5: 11,  # Social History
            6: 22,  # Cardiovascular Health
            7: 4,   # Respiratory Health
            8: 18,  # Gastrointestinal Health
            9: 9,   # History of Infectious Disease
            10: 3,  # History of Skin Health
            11: 10, # History of Autoimmunity
            12: 14, # Sleep History
            13: 11, # Diabetes Health History
            14: 6,  # Dental History
            15: 18, # Female Hormone Health
            16: 7,  # Male Hormone Health
            17: 9,  # Surgical History
            18: 11, # Mental Health History
            19: 3,  # History of Cancer or Chemotherapy
            20: 10, # Potential Risk for Mold Toxin Exposure
            21: 15, # Potential Risk for Chemical or Metal Exposure
            22: 6,  # Muscle and Skeletal Health
            23: 6   # Use of Supplements
        }
        
        # Determine which sections apply based on pre-screening
        applicable_sections = list(range(24))
        if self.responses.get('pre_is_female') == 'on':
            applicable_sections.remove(16)  # Remove Male Hormone Health
        else:
            applicable_sections.remove(15)  # Remove Female Hormone Health
            
        if self.responses.get('pre_has_dementia_history') != 'on':
            applicable_sections.remove(1)  # Remove Dementia Diagnosis
            
        # Calculate total applicable questions
        total_questions = sum(section_questions[i] for i in applicable_sections)
        
        # Count answered questions (excluding pre-screening and navigation fields)
        answered_questions = sum(
            1 for key, value in self.responses.items()
            if (
                (value is True or value == 'on')  # Handle both boolean True and string 'on'
                and not key.startswith('pre_')
                and key not in ['next_step', 'prev_step', 'save_exit', 'submit_form']
            )
        )
        
        return round((answered_questions / total_questions) * 100) if total_questions > 0 else 0 