from datetime import datetime
from .db import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)  # autoevaluacion, evaluacion_estudiante, lista_cotejo
    periodo_id = db.Column(db.Integer, db.ForeignKey('evaluation_periods.id'), nullable=False)
    evaluado_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Null for self-evaluations
    curso_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)  # For student evaluations
    status = db.Column(db.String(20), default='borrador')  # borrador, pendiente, validado, observado, rechazado
    comentarios = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)
    validated_at = db.Column(db.DateTime, nullable=True)
    validated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    responses = db.relationship('EvaluationResponse', backref='evaluation', lazy=True, cascade='all, delete-orphan')
    period = db.relationship('EvaluationPeriod', backref='evaluations')
    validated_by = db.relationship('User', foreign_keys=[validated_by_id])
    
    def calculate_score(self):
        """Calculate the total score based on responses."""
        total_score = 0
        max_possible = 0
        
        for response in self.responses:
            if response.score is not None:
                total_score += response.score
                max_possible += response.criteria.max_score
        
        return total_score, max_possible
    
    def __repr__(self):
        return f'<Evaluation {self.id} - {self.tipo} - {self.status}>'

class EvaluationPeriod(db.Model):
    __tablename__ = 'evaluation_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<EvaluationPeriod {self.name}>'

class EvaluationResponse(db.Model):
    __tablename__ = 'evaluation_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('evaluation_criteria.id'), nullable=False)
    response_value = db.Column(db.String(50), nullable=True)  # For scale-based responses
    score = db.Column(db.Float, nullable=True)  # Numeric score if applicable
    comments = db.Column(db.Text, nullable=True)
    
    # Relationship
    criteria = db.relationship('EvaluationCriteria')
    
    def __repr__(self):
        return f'<EvaluationResponse {self.id} - Criteria {self.criteria_id}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('evaluation_periods.id'), nullable=False)
    
    # Relationships
    teacher = db.relationship('User', backref='courses')
    students = db.relationship('StudentCourse', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.code} - {self.name}>'

class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Relationship
    student = db.relationship('User', backref='enrolled_courses')
    
    def __repr__(self):
        return f'<StudentCourse {self.student_id} - {self.course_id}>'