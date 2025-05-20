# app/__init__.py
from flask import Flask, session, redirect, url_for
from config import Config as AppConfig # Renombrar para evitar conflicto con Flask.Config
from app.models.user import User # Para el context_processor
import datetime

def get_nav_items(user_role_id=None):
    # Si no hay user_id en sesión, no mostrar items de navegación protegidos
    if not session.get('user_id'):
        return []

    # Base nav_items 
    # Los href usarán url_for con el prefijo del blueprint, ej. 'main.dashboard'
    
    # Items comunes para la mayoría de los roles logueados (o todos)
    common_nav_items = [
        {"href": url_for('main.dashboard'), "title": "Dashboard", "icon_svg_name": "home"},
        {"href": url_for('main.self_evaluation'), "title": "Autoevaluación", "icon_svg_name": "user-square-2"},
        {"href": url_for('main.results'), "title": "Resultados", "icon_svg_name": "bar-chart-4"},
        {"href": url_for('main.incidents'), "title": "Incidencias", "icon_svg_name": "alert-circle"},
    ]

    # Items específicos por rol
    role_specific_items = []

    if user_role_id == 1 or user_role_id == 5: # Admin o Developer
        role_specific_items = [
            {"href": url_for('main.student_evaluation'), "title": "Evaluar Docentes", "icon_svg_name": "clipboard-list"}, # Admin podría necesitar ver esto también
            {"href": url_for('main.checklist_evaluation'), "title": "Lista de Cotejo", "icon_svg_name": "check-square"},
            {"href": url_for('main.validation'), "title": "Validación Eval.", "icon_svg_name": "shield-check"},
            {"href": url_for('main.roles'), "title": "Usuarios y Roles", "icon_svg_name": "users"}, # Cambiado de "Roles y Permisos"
            # Nuevas rutas de administración:
            {"href": url_for('admin.manage_criteria'), "title": "Adm. Criterios", "icon_svg_name": "list-checks"}, # Usando un ícono diferente
            {"href": url_for('admin.manage_collaborator_types'), "title": "Tipos Colaborador", "icon_svg_name": "user-cog"}, # Ícono sugerido
            {"href": url_for('admin.manage_contract_types'), "title": "Tipos Contrato", "icon_svg_name": "file-text"},
            {"href": url_for('admin.manage_collaborators'), "title": "Adm. Colaboradores", "icon_svg_name": "users-round"}, # Ícono sugerido (nuevo)
            # Ícono sugerido
            # Podrías añadir un enlace general a "/admin" o más secciones aquí
        ]
        # Los administradores y desarrolladores ven todos los items comunes más los suyos específicos
        return common_nav_items + role_specific_items

    elif user_role_id == 2: # Docente
        # Los docentes ven los items comunes (ya incluye autoevaluación y resultados)
        # No necesitan items adicionales específicos listados aquí si common_nav_items ya los cubre.
        # Si tuvieran algo único, se añadiría aquí.
        return common_nav_items
        
    elif user_role_id == 4: # Estudiante
        role_specific_items = [
            {"href": url_for('main.student_evaluation'), "title": "Evaluar Docentes", "icon_svg_name": "clipboard-list"},
        ]
        # Estudiantes ven dashboard, evaluar docentes, e incidencias (de common_nav_items)
        # Filtramos common_nav_items para que no vean autoevaluación o resultados generales si no aplica.
        student_common_items = [
            item for item in common_nav_items 
            if item["title"] in ["Dashboard", "Incidencias"] # Solo estos de los comunes
        ]
        return student_common_items + role_specific_items
    
    # Por defecto, para roles no especificados o si algo falla, solo el dashboard
    return [{"href": url_for('main.dashboard'), "title": "Dashboard", "icon_svg_name": "home"}]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración de la aplicación
    app.config.from_object(AppConfig) # Carga desde config.py
    app.config['SECRET_KEY'] = AppConfig.SECRET_KEY 
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

    # Registrar Blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.admin import admin_bp # Asegúrate que este blueprint esté importado
    app.register_blueprint(admin_bp)   


    @app.context_processor
    def inject_global_vars():
        user_id = session.get('user_id')
        user_role_id = session.get('user_role_id')
        current_user_role_display = User.get_role_name_by_id(user_role_id) if user_id else "Invitado"
        
        nav_items_list = []
        if user_id: 
            nav_items_list = get_nav_items(user_role_id)

        return dict(
            nav_items=nav_items_list,
            current_user_role_display=current_user_role_display,
            now=datetime.datetime.utcnow(),
            show_sidebar_header=(user_id is not None)
        )

    return app