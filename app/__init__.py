# app/__init__.py
from flask import Flask, session, redirect, url_for
from config import Config as AppConfig # Renombrar para evitar conflicto con Flask.Config
from app.models.user import User # Para el context_processor
import datetime

def get_nav_items(user_role_id=None):
    # Si no hay user_id en sesión, no mostrar items de navegación protegidos
    if not session.get('user_id'):
        return []

    # Base nav_items (ejemplo, ajustar según tus necesidades y roles)
    # Los href usarán url_for con el prefijo del blueprint, ej. 'main.dashboard'
    nav_items_all = [
        {"href": url_for('main.dashboard'), "title": "Dashboard", "icon_svg_name": "home"},
        {"href": url_for('main.self_evaluation'), "title": "Autoevaluación", "icon_svg_name": "user-square-2"},
        {"href": url_for('main.student_evaluation'), "title": "Evaluar Docentes", "icon_svg_name": "clipboard-list"},
        {"href": url_for('main.checklist_evaluation'), "title": "Lista de Cotejo", "icon_svg_name": "check-square"},
        {"href": url_for('main.results'), "title": "Resultados", "icon_svg_name": "bar-chart-4"},
        {"href": url_for('main.incidents'), "title": "Incidencias", "icon_svg_name": "alert-circle"},
        {"href": url_for('main.validation'), "title": "Validación", "icon_svg_name": "shield-check"},
        {"href": url_for('main.roles'), "title": "Roles y Permisos", "icon_svg_name": "users"},
    ]
    # Lógica de filtrado de roles (similar a como la tenías antes)
    if user_role_id == 1 or user_role_id == 5: # Admin o Developer
        return nav_items_all
    elif user_role_id == 2: # Docente
        return [
            {"href": url_for('main.dashboard'), "title": "Dashboard", "icon_svg_name": "home"},
            {"href": url_for('main.self_evaluation'), "title": "Autoevaluación", "icon_svg_name": "user-square-2"},
            {"href": url_for('main.results'), "title": "Resultados", "icon_svg_name": "bar-chart-4"},
            {"href": url_for('main.incidents'), "title": "Incidencias", "icon_svg_name": "alert-circle"},
        ]
    # ... (más roles)
    return [{"href": url_for('main.dashboard'), "title": "Dashboard", "icon_svg_name": "home"}]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configuración de la aplicación
    app.config.from_object(AppConfig) # Carga desde config.py
    app.config['SECRET_KEY'] = AppConfig.SECRET_KEY # Asegúrate que SECRET_KEY esté en config.py
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

    # Registrar Blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp) # Si usaste url_prefix='/auth', las rutas serán /auth/login, etc.
                                    # Si no, serán /login, /register

    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_global_vars():
        user_id = session.get('user_id')
        user_role_id = session.get('user_role_id')
        current_user_role_display = User.get_role_name_by_id(user_role_id) if user_id else "Invitado"
        
        nav_items_list = []
        if user_id: # Solo generar nav_items si el usuario está logueado
            nav_items_list = get_nav_items(user_role_id)

        return dict(
            nav_items=nav_items_list,
            current_user_role_display=current_user_role_display,
            now=datetime.datetime.utcnow(),
            show_sidebar_header=(user_id is not None)
        )

    return app