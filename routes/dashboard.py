from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

from models.db import db
from models.evaluation import Evaluation, EvaluationPeriod
from models.incident import Incident
from models.checklist import Checklist

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Get active evaluation period
    active_period = EvaluationPeriod.query.filter_by(active=True).first()
    
    # Dashboard statistics based on user role
    stats = {}
    
    # General statistics for all users
    if active_period:
        # Self-evaluations
        self_eval_count = Evaluation.query.filter_by(
            evaluado_id=current_user.id,
            tipo='autoevaluacion',
            periodo_id=active_period.id
        ).count()
        
        # Pending tasks
        if current_user.has_role('validador'):
            pending_validations = Evaluation.query.filter_by(
                status='pendiente',
                periodo_id=active_period.id
            ).count()
            stats['pending_validations'] = pending_validations
        
        if current_user.has_role('evaluador'):
            pending_evaluations = Checklist.query.filter_by(
                evaluador_id=current_user.id,
                status='borrador',
                periodo_id=active_period.id
            ).count()
            stats['pending_evaluations'] = pending_evaluations
        
        # For students
        if current_user.tipo_usuario == 'estudiante':
            # Count how many teacher evaluations are pending
            from models.evaluation import StudentCourse, Course
            
            # Get student's courses
            student_courses = StudentCourse.query.filter_by(
                student_id=current_user.id
            ).all()
            
            course_ids = [sc.course_id for sc in student_courses]
            courses = Course.query.filter(
                Course.id.in_(course_ids),
                Course.period_id == active_period.id
            ).all()
            
            teacher_ids = [course.teacher_id for course in courses]
            
            # Count completed evaluations
            completed_evals = Evaluation.query.filter(
                Evaluation.evaluador_id == current_user.id,
                Evaluation.evaluado_id.in_(teacher_ids),
                Evaluation.tipo == 'evaluacion_estudiante',
                Evaluation.periodo_id == active_period.id
            ).count()
            
            stats['completed_teacher_evals'] = completed_evals
            stats['total_teacher_evals'] = len(teacher_ids)
        
        # Incidents
        open_incidents = Incident.query.filter_by(
            reported_by_id=current_user.id,
            status='abierto'
        ).count()
        
        assigned_incidents = Incident.query.filter_by(
            assigned_to_id=current_user.id,
            status='en_proceso'
        ).count()
        
        # Add stats to dictionary
        stats['self_eval_count'] = self_eval_count
        stats['open_incidents'] = open_incidents
        stats['assigned_incidents'] = assigned_incidents
        stats['active_period'] = active_period
    
    # Get recent activities
    from models.audit_log import AuditLog
    
    recent_activities = AuditLog.query.filter_by(
        user_id=current_user.id
    ).order_by(AuditLog.created_at.desc()).limit(5).all()
    
    # Get any notifications or alerts
    notifications = []
    
    # Check for evaluations close to deadline
    if active_period and (active_period.end_date - datetime.utcnow()).days <= 7:
        notifications.append({
            'type': 'warning',
            'message': f'El periodo de evaluación "{active_period.name}" finaliza en menos de 7 días.'
        })
    
    # Check for pending items
    if stats.get('pending_evaluations', 0) > 0:
        notifications.append({
            'type': 'info',
            'message': f'Tiene {stats["pending_evaluations"]} evaluaciones pendientes por completar.'
        })
    
    return render_template(
        'dashboard/index.html',
        stats=stats,
        recent_activities=recent_activities,
        notifications=notifications
    )