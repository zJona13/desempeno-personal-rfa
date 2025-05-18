from datetime import datetime
from .db import db

class Checklist(db.Model):
    __tablename__ = 'checklists'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    template_id = db.Column(db.Integer, db.ForeignKey('checklist_templates.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluado_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='borrador')  # borrador, pendiente, validado, observado, rechazado
    periodo_id = db.Column(db.Integer, db.ForeignKey('evaluation_periods.id'), nullable=False)
    total_score = db.Column(db.Float, nullable=True)
    max_possible_score = db.Column(db.Float, nullable=True)
    observations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)
    validated_at = db.Column(db.DateTime, nullable=True)
    validated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    template = db.relationship('ChecklistTemplate')
    evaluador = db.relationship('User', foreign_keys=[evaluador_id], backref='checklists_evaluated')
    evaluado = db.relationship('User', foreign_keys=[evaluado_id], backref='checklists_received')
    period = db.relationship('EvaluationPeriod')
    items = db.relationship('ChecklistItem', backref='checklist', lazy=True, cascade='all, delete-orphan')
    validated_by = db.relationship('User', foreign_keys=[validated_by_id])
    
    def calculate_score(self):
        """Calculate the total score based on items."""
        self.total_score = sum(item.score for item in self.items if item.score is not None)
        self.max_possible_score = sum(item.criteria.weight * item.criteria.max_score for item in self.items)
        return self.total_score, self.max_possible_score
    
    def __repr__(self):
        return f'<Checklist {self.id} - {self.title}>'

class ChecklistTemplate(db.Model):
    __tablename__ = 'checklist_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    applicable_to = db.Column(db.String(50), nullable=False)  # docente, administrativo
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    criteria = db.relationship('ChecklistCriteria', backref='template', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ChecklistTemplate {self.name}>'

class ChecklistCriteria(db.Model):
    __tablename__ = 'checklist_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('checklist_templates.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Float, default=1.0)
    max_score = db.Column(db.Float, default=5.0)
    order = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<ChecklistCriteria {self.id} - {self.text[:20]}...>'

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'
    
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('checklist_criteria.id'), nullable=False)
    score = db.Column(db.Float, nullable=True)
    evidence = db.Column(db.Text, nullable=True)  # Description or reference to evidence
    comments = db.Column(db.Text, nullable=True)
    
    # Relationship
    criteria = db.relationship('ChecklistCriteria')
    
    def __repr__(self):
        return f'<ChecklistItem {self.id}>'