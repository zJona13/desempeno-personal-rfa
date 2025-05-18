from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime

from models.db import db
from models.user import User
from models.evaluation import Evaluation, EvaluationPeriod, EvaluationResponse
from models.evaluation_criteria import EvaluationCriteria, CriteriaCategory
from models.audit_log import AuditLog

self_evaluation_bp = Blueprint('self_evaluation', __name__, url_prefix='/autoevaluacion')

@self_evaluation_bp.route('/')
@login_required
def index():
    # Get active period
    active_period = EvaluationPeriod.query.filter_by(active=True).first()
    
    if not active_period:
        flash('No hay un periodo de evaluación activo en este momento.', 'warning')
        return render_template('self_evaluation/no_active_period.html')
    
    # Check if user has already submitted an evaluation for this period
    existing_eval = Evaluation.query.filter_by(
        evaluado_id=current_user.id,
        periodo_id=active_period.id,
        tipo='autoevaluacion'
    ).first()
    
    if existing_eval:
        # Show the evaluation details/status
        return render_template('self_evaluation/status.html', 
                              evaluation=existing_eval, 
                              period=active_period)
    
    # No existing evaluation, show the form to create one
    return redirect(url_for('self_evaluation.create'))

@self_evaluation_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Get active period
    active_period = EvaluationPeriod.query.filter_by(active=True).first()
    
    if not active_period:
        flash('No hay un periodo de evaluación activo en este momento.', 'warning')
        return redirect(url_for('self_evaluation.index'))
    
    # Check if user has already submitted an evaluation for this period
    existing_eval = Evaluation.query.filter_by(
        evaluado_id=current_user.id,
        periodo_id=active_period.id,
        tipo='autoevaluacion'
    ).first()
    
    if existing_eval and existing_eval.status != 'borrador':
        flash('Ya ha enviado su autoevaluación para este periodo.', 'info')
        return redirect(url_for('self_evaluation.index'))
    
    # Get criteria categories and criteria for self-evaluation
    categories = CriteriaCategory.query.filter_by(
        evaluation_type='autoevaluacion',
        active=True
    ).order_by(CriteriaCategory.order).all()
    
    if request.method == 'POST':
        is_draft = 'save_draft' in request.form
        
        # Create new evaluation or use existing draft
        if existing_eval:
            evaluation = existing_eval
        else:
            evaluation = Evaluation(
                tipo='autoevaluacion',
                periodo_id=active_period.id,
                evaluado_id=current_user.id,
                status='borrador'
            )
            db.session.add(evaluation)
            db.session.flush()  # Get the ID without committing
        
        # Process each criteria response
        for key, value in request.form.items():
            if key.startswith('criteria_'):
                criteria_id = int(key.split('_')[1])
                
                # Check if response already exists
                existing_response = EvaluationResponse.query.filter_by(
                    evaluation_id=evaluation.id,
                    criteria_id=criteria_id
                ).first()
                
                if existing_response:
                    # Update existing response
                    existing_response.response_value = value
                    existing_response.score = calculate_score(value)
                else:
                    # Create new response
                    response = EvaluationResponse(
                        evaluation_id=evaluation.id,
                        criteria_id=criteria_id,
                        response_value=value,
                        score=calculate_score(value)
                    )
                    db.session.add(response)
            
            # Handle comments
            elif key.startswith('comment_'):
                criteria_id = int(key.split('_')[1])
                
                existing_response = EvaluationResponse.query.filter_by(
                    evaluation_id=evaluation.id,
                    criteria_id=criteria_id
                ).first()
                
                if existing_response:
                    existing_response.comments = value
        
        # Update evaluation status and timestamp
        if not is_draft:
            evaluation.status = 'pendiente'
            evaluation.submitted_at = datetime.utcnow()
            
            # Validate all questions are answered
            all_criteria_ids = [c.id for category in categories for c in category.criteria if c.active]
            responses = EvaluationResponse.query.filter_by(evaluation_id=evaluation.id).all()
            response_criteria_ids = [r.criteria_id for r in responses if r.response_value]
            
            if set(all_criteria_ids) != set(response_criteria_ids):
                flash('Por favor responda todas las preguntas antes de enviar.', 'error')
                return render_template('self_evaluation/form.html', 
                                      categories=categories, 
                                      period=active_period,
                                      evaluation=evaluation)
            
            action_desc = 'Autoevaluación enviada para validación'
        else:
            action_desc = 'Autoevaluación guardada como borrador'
        
        # Add to audit log
        log = AuditLog(
            user_id=current_user.id,
            action='submit_evaluation' if not is_draft else 'save_draft',
            module='self_evaluation',
            description=action_desc,
            resource_type='evaluation',
            resource_id=evaluation.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        
        db.session.commit()
        
        if not is_draft:
            flash('Su autoevaluación ha sido enviada exitosamente.', 'success')
        else:
            flash('Su autoevaluación ha sido guardada como borrador.', 'success')
        
        return redirect(url_for('self_evaluation.index'))
    
    # If we have an existing draft, populate the form with saved responses
    responses = {}
    if existing_eval:
        for response in existing_eval.responses:
            responses[response.criteria_id] = {
                'value': response.response_value,
                'comments': response.comments
            }
    
    return render_template('self_evaluation/form.html', 
                          categories=categories, 
                          period=active_period,
                          responses=responses,
                          evaluation=existing_eval)

@self_evaluation_bp.route('/<int:evaluation_id>')
@login_required
def view(evaluation_id):
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    
    # Security check - users can only view their own evaluations or if they are validators
    if evaluation.evaluado_id != current_user.id and not current_user.has_permission('validate_evaluations'):
        flash('No tiene permiso para ver esta evaluación.', 'error')
        return redirect(url_for('self_evaluation.index'))
    
    # Organize responses by category for display
    categories = {}
    for response in evaluation.responses:
        category = response.criteria.category
        
        if category.id not in categories:
            categories[category.id] = {
                'name': category.name,
                'description': category.description,
                'criteria': []
            }
        
        categories[category.id]['criteria'].append({
            'text': response.criteria.text,
            'response': response.response_value,
            'comments': response.comments
        })
    
    return render_template('self_evaluation/view.html', 
                          evaluation=evaluation, 
                          categories=categories)

def calculate_score(response_value):
    """Calculate numeric score from response value."""
    # This will depend on the scale used
    score_mapping = {
        'nunca': 0,
        'a_veces': 2.5,
        'siempre': 5,
        'si': 5,
        'no': 0
    }
    
    return score_mapping.get(response_value, None)