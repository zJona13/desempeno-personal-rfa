from datetime import datetime
from .db import db

class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # tecnica, administrativa, academica
    priority = db.Column(db.String(20), default='media')  # baja, media, alta, critica
    status = db.Column(db.String(20), default='abierto')  # abierto, en_proceso, resuelto, cerrado
    reported_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    related_evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    comments = db.relationship('IncidentComment', backref='incident', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('IncidentAttachment', backref='incident', lazy=True, cascade='all, delete-orphan')
    related_evaluation = db.relationship('Evaluation', backref='incidents')
    
    def __repr__(self):
        return f'<Incident {self.id} - {self.title}>'

class IncidentComment(db.Model):
    __tablename__ = 'incident_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='incident_comments')
    
    def __repr__(self):
        return f'<IncidentComment {self.id}>'

class IncidentAttachment(db.Model):
    __tablename__ = 'incident_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(100), nullable=True)
    filesize = db.Column(db.Integer, nullable=True)  # In bytes
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    uploaded_by = db.relationship('User', backref='incident_attachments')
    
    def __repr__(self):
        return f'<IncidentAttachment {self.id} - {self.filename}>'