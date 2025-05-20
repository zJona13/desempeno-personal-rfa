# app/routes/main.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash # Asegúrate que flash esté importado
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/') # Ruta raíz
def index(): 
    if not session.get('user_id'):
        return redirect(url_for('auth.login')) # Si no hay sesión, va al login
    return redirect(url_for('main.dashboard')) # Si hay sesión, va al dashboard

@main_bp.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login')) 

    user_name = session.get('user_name', 'Usuario')
    greeting = "Hola" 

    stats = {
        "evaluaciones_pendientes": 5, 
        "trend_evaluaciones": {"is_positive": True, "value": 10},
        "incidencias_activas": 2,
        "trend_incidencias": {"is_positive": False, "value": 5}, 
        "validaciones_pendientes": 3,
        "total_resultados": 150,
        "trend_resultados": {"is_positive": True, "value": 12}
    }
    
    user_role_id = session.get('user_role_id')
    modules = []
    
    if user_role_id == 1 or user_role_id == 5: # Admin o Developer
        modules = [
            {"title": "Autoevaluación Personal", "description": "Complete o revise su autoevaluación.", "href": url_for('main.self_evaluation'), "icon_svg_name": "user-square-2", "color": "bg-blue-100 text-blue-600 dark:bg-blue-700 dark:text-blue-200"},
            {"title": "Evaluar con Lista de Cotejo", "description": "Realice evaluaciones usando criterios definidos.", "href": url_for('main.checklist_evaluation'), "icon_svg_name": "clipboard-list", "color": "bg-green-100 text-green-600 dark:bg-green-700 dark:text-green-200"},
            {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('main.incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
            {"title": "Validación de Evaluaciones", "description": "Revise y valide evaluaciones.", "href": url_for('main.validation'), "icon_svg_name": "shield-check", "color": "bg-purple-100 text-purple-600 dark:bg-purple-700 dark:text-purple-200"},
            {"title": "Administrar Roles", "description": "Gestione roles y permisos de usuarios.", "href": url_for('main.roles'), "icon_svg_name": "users", "color": "bg-red-100 text-red-600 dark:bg-red-700 dark:text-red-200"},
            {"title": "Ver Resultados", "description": "Consulte los resultados de las evaluaciones.", "href": url_for('main.results'), "icon_svg_name": "bar-chart-4", "color": "bg-indigo-100 text-indigo-600 dark:bg-indigo-700 dark:text-indigo-200"}
        ]
    elif user_role_id == 2: # Docente
         modules = [
            {"title": "Autoevaluación Personal", "description": "Complete o revise su autoevaluación.", "href": url_for('main.self_evaluation'), "icon_svg_name": "user-square-2", "color": "bg-blue-100 text-blue-600 dark:bg-blue-700 dark:text-blue-200"},
            {"title": "Ver Resultados", "description": "Consulte sus resultados de evaluaciones.", "href": url_for('main.results'), "icon_svg_name": "bar-chart-4", "color": "bg-indigo-100 text-indigo-600 dark:bg-indigo-700 dark:text-indigo-200"},
            {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('main.incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
        ]
    elif user_role_id == 4: # Estudiante
        modules = [
             {"title": "Evaluación Docente", "description": "Evalúe el desempeño de sus docentes.", "href": url_for('main.student_evaluation'), "icon_svg_name": "clipboard-list", "color": "bg-green-100 text-green-600 dark:bg-green-700 dark:text-green-200"},
             {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('main.incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
        ]

    return render_template('dashboard.html', greeting=greeting, user_name=user_name, stats=stats, modules=modules)

@main_bp.route('/self_evaluation')
def self_evaluation():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    
    evaluations = [
        {"id": 1, "title": "Autoevaluación Semestral 2025-I", "status": "active", "status_text": "Pendiente", "status_icon": "clock", "status_bg_color": "bg-yellow-100", "status_text_color":"text-yellow-700", "due_date": "2025-06-15", "criteria_count": 25, "estimated_time_minutes": 30, "action_button_text": "Iniciar Evaluación", "action_button_variant":"primary", "action_url_param": 1},
        {"id": 2, "title": "Autoevaluación Anual 2024", "status": "completed", "status_text": "Completado", "status_icon": "check-circle-2", "status_bg_color": "bg-green-100", "status_text_color":"text-green-700", "completed_date": "2024-12-01", "criteria_count": 20, "score": "92%", "action_button_text": "Ver Resultados", "action_button_variant":"outline", "action_url_param": 2},
    ]
    show_form_param = request.args.get('evaluation_id')
    show_form = bool(show_form_param) 
    evaluation_data = None
    if show_form: 
        evaluation_data = {
            "title": "Autoevaluación Semestral 2025-I",
            "criteria": [
                {"id": 1, "category": "Planificación Curricular", "text": "Elabora el sílabo considerando el perfil del egresado.", "value": None, "comment": ""},
                {"id": 2, "category": "Planificación Curricular", "text": "Presenta el sílabo a los estudiantes al inicio del semestre.", "value": None, "comment": ""},
                {"id": 3, "category": "Proceso de Enseñanza-Aprendizaje", "text": "Utiliza estrategias de enseñanza activas y participativas.", "value": None, "comment": ""},
            ]
        }
    return render_template('self-evaluation.html', evaluations=evaluations, show_form=show_form, evaluation_data=evaluation_data)

@main_bp.route('/student_evaluation')
def student_evaluation():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    evaluations_pending = [
        {"id": 1, "subject_name": "Matemática Aplicada I", "teacher_name": "Dr. Alan Turing", "section": "A"},
        {"id": 2, "subject_name": "Desarrollo Web Fullstack", "teacher_name": "Ing. Ada Lovelace", "section": "B"},
    ]
    return render_template('student-evaluation.html', evaluations_pending=evaluations_pending)

@main_bp.route('/checklist_evaluation')
def checklist_evaluation():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    pending_evaluations = [
        {"id": 101, "name": "Carlos Santana", "role": "Docente Contratado", "department": "Ciencias Básicas"},
    ]
    completed_evaluations = [
        {"id": 201, "name": "Luisa Pérez", "role": "Docente Principal", "department": "Ingeniería", "score": "88%", "completed_date": "2025-05-10"},
    ]
    return render_template('checklist-evaluation.html', pending_evaluations=pending_evaluations, completed_evaluations=completed_evaluations)

@main_bp.route('/results')
def results():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    summary = {
        "pedagogico": {"score_percent": 85, "text_color": "text-green-600"},
        "academico": {"score_percent": 90, "text_color": "text-green-600"},
        "gestion": {"score_percent": 75, "text_color": "text-yellow-600"},
        "global": {"score_percent": 83, "text_color": "text-green-600"}
    }
    return render_template('results.html', summary=summary)

@main_bp.route('/incidents')
def incidents():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    incidents_data = [
        {"id": 1, "title": "Error al cargar notas", "reported_date": "2025-05-18", "type": "Sistema", "status": "En proceso", "description_summary": "Los estudiantes no pueden ver sus calificaciones...", "status_color_class": "bg-yellow-500 text-white"},
        {"id": 2, "title": "Aula sin proyector", "reported_date": "2025-05-15", "type": "Infraestructura", "status": "Resuelto", "description_summary": "Se solicitó un proyector para el aula C-102.", "status_color_class": "bg-green-100 text-green-700"},
    ]
    return render_template('incidents.html', incidents=incidents_data)

@main_bp.route('/validation')
def validation():
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    autoevaluaciones_pendientes = [
        {"id": 301, "name": "Ana Torres", "type": "Autoevaluación Docente", "role_department": "Docente - Idiomas", "submitted_date": "2025-05-20"},
    ]
    listas_cotejo_pendientes = [] # Ejemplo vacío
    validaciones_recientes = [
        {"id": 401, "name": "Pedro Castillo", "type": "Autoevaluación", "validated_date": "2025-05-19", "status": "Aprobado", "status_icon": "check-circle-2", "status_color_class": "text-green-600 bg-green-100", "score": "90%"},
    ]
    return render_template('validation.html', 
                           autoevaluaciones_pendientes=autoevaluaciones_pendientes, 
                           listas_cotejo_pendientes=listas_cotejo_pendientes, 
                           validaciones_recientes=validaciones_recientes)

@main_bp.route('/roles') 
def roles(): 
    if not session.get('user_id'): 
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('auth.login'))
    active_tab = request.args.get('tab', 'roles')
    search_query = request.args.get('q', '')
    
    roles_data = [
        {"id": 1, "name": "Administrador", "description": "Acceso total al sistema", "users": 2, "color":"destructive"},
        {"id": 2, "name": "Docente", "description": "Realiza autoevaluación, gestiona cursos", "users": 15, "color":"primary"},
        {"id": 4, "name": "Estudiante", "description": "Evalúa a docentes", "users": 250, "color":"secondary"},
    ]
    users_data = [
        {"id": 1, "name": "Jonatan Ching", "email": "jching@iesrfa.edu", "role": "Administrador", "status": "Activo"},
        {"id": 2, "name": "Roger Zavaleta", "email": "rzavaleta@iesrfa.edu", "role": "Docente", "status": "Activo"},
    ]

    all_roles_for_matrix = roles_data 
    permissions_matrix = [
        {"id": "mod1", "module": "Gestión de Usuarios", "actions": ["crear", "editar", "eliminar", "ver"]},
        {"id": "mod2", "module": "Evaluaciones", "actions": ["realizar_autoevaluacion", "evaluar_pares", "validar_evaluacion"]},
    ]
    
    def get_role_permission(role_name, module_name, action_name):
        if role_name == "Administrador":
            return True
        if role_name == "Docente" and module_name == "Evaluaciones" and action_name == "realizar_autoevaluacion":
            return True
        return False

    return render_template('roles.html', 
                           active_tab=active_tab, 
                           search_query=search_query,
                           roles=roles_data, 
                           users=users_data,
                           all_roles_for_matrix=all_roles_for_matrix,
                           permissions_matrix=permissions_matrix,
                           get_role_permission=get_role_permission, 
                           validation_errors_for_dialog=None)