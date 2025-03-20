from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', backref='client', lazy=True)
    lab_results = db.relationship('LabResult', backref='client', lazy=True)

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
    q1 = db.Column(db.Boolean)
    q2 = db.Column(db.Boolean)
    q3 = db.Column(db.Boolean)
    q4 = db.Column(db.Boolean)
    q5 = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 