from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .db import db
from .role import user_roles

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    tipo_usuario = db.Column(db.String(20), default='docente')  # docente, administrativo, estudiante
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    evaluations_submitted = db.relationship('Evaluation', backref='evaluado', lazy='dynamic', 
                                           foreign_keys='Evaluation.evaluado_id')
    evaluations_reviewed = db.relationship('Evaluation', backref='evaluador', lazy='dynamic',
                                          foreign_keys='Evaluation.evaluador_id')
    incidents_reported = db.relationship('Incident', backref='reported_by', lazy='dynamic',
                                       foreign_keys='Incident.reported_by_id')
    incidents_assigned = db.relationship('Incident', backref='assigned_to', lazy='dynamic',
                                       foreign_keys='Incident.assigned_to_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)
    
    def has_permission(self, permission_name):
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False
    
    def __repr__(self):
        return f'<User {self.email}>'