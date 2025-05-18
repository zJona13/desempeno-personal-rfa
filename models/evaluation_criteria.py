from .db import db

class EvaluationCriteria(db.Model):
    __tablename__ = 'evaluation_criteria'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('criteria_categories.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # escala, si_no, numerica
    options = db.Column(db.Text, nullable=True)  # JSON string of possible options for scale-based criteria
    weight = db.Column(db.Float, default=1.0)
    max_score = db.Column(db.Float, default=5.0)
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    
    # Relationships
    category = db.relationship('CriteriaCategory', backref='criteria')
    
    def __repr__(self):
        return f'<EvaluationCriteria {self.id} - {self.text[:20]}...>'

class CriteriaCategory(db.Model):
    __tablename__ = 'criteria_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    evaluation_type = db.Column(db.String(50), nullable=False)  # autoevaluacion, evaluacion_estudiante, lista_cotejo
    order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CriteriaCategory {self.name}>'