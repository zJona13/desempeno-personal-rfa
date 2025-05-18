from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import datetime

from models.db import db
from models.user import User
from models.role import Role
from models.permission import Permission
from models.evaluation import Evaluation
from models.evaluation_criteria import EvaluationCriteria
from models.incident import Incident
from models.checklist import Checklist
from models.audit_log import AuditLog

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.self_evaluation import self_evaluation_bp
# from routes.student_evaluation import student_evaluation_bp
# from routes.incidents import incidents_bp
# from routes.checklists import checklists_bp
# from routes.admin import admin_bp
# from routes.validation import validation_bp
# from routes.results import results_bp

load_dotenv()

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configure database
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-replace-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/sistema_evaluacion')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(self_evaluation_bp)
# app.register_blueprint(student_evaluation_bp)
# app.register_blueprint(incidents_bp)
# app.register_blueprint(checklists_bp)
# app.register_blueprint(admin_bp)
# app.register_blueprint(validation_bp)
# app.register_blueprint(results_bp)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

# Context processors
@app.context_processor
def utility_processor():
    def format_date(date):
        if date:
            return date.strftime('%d/%m/%Y')
        return ""
    
    def user_has_permission(permission_name):
        if not current_user.is_authenticated:
            return False
        return current_user.has_permission(permission_name)
    
    return dict(
        format_date=format_date,
        user_has_permission=user_has_permission,
        current_year=datetime.now().year
    )

# # Initialize database
# @app.before_first_request
# def create_tables():
#     db.create_all()
#     # Initialize default roles and permissions if not exists
#     if not Role.query.filter_by(name='admin').first():
#         admin_role = Role(name='admin', description='Administrador del sistema')
#         db.session.add(admin_role)
        
#         # Add default admin user if not exists
#         if not User.query.filter_by(email='admin@iesrfa.edu').first():
#             admin_user = User(
#                 nombre='Administrador',
#                 apellido='Sistema',
#                 email='admin@iesrfa.edu',
#                 active=True
#             )
#             admin_user.set_password('admin123')  # Change in production
#             admin_user.roles.append(admin_role)
#             db.session.add(admin_user)
        
#         db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)