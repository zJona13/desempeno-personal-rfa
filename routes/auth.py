from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import ipaddress

from models.db import db
from models.user import User
from models.audit_log import AuditLog
from forms.auth import LoginForm, PasswordResetForm, PasswordChangeForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.active:
                flash('Su cuenta está desactivada. Contacte al administrador.', 'error')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=form.remember.data)
            
            # Update last login time
            user.last_login = datetime.utcnow()
            
            # Log the login action
            log = AuditLog(
                user_id=user.id,
                action='login',
                module='auth',
                description=f'Inicio de sesión exitoso',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                resource_type='user',
                resource_id=user.id
            )
            db.session.add(log)
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                # Validate next parameter to prevent open redirect
                try:
                    if next_page.startswith('/') and not next_page.startswith('//'):
                        return redirect(next_page)
                except:
                    pass
            
            return redirect(url_for('dashboard.index'))
        else:
            flash('Credenciales inválidas. Por favor intente nuevamente.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # Log the logout action
    log = AuditLog(
        user_id=current_user.id,
        action='logout',
        module='auth',
        description=f'Cierre de sesión',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        resource_type='user',
        resource_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # In a real app, this would send a password reset email
    # For this demo, we'll keep it simple
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Se ha enviado un enlace de recuperación a su correo electrónico.', 'success')
        else:
            # Don't reveal that the user doesn't exist
            flash('Se ha enviado un enlace de recuperación a su correo electrónico.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            
            # Log the password change
            log = AuditLog(
                user_id=current_user.id,
                action='password_change',
                module='auth',
                description=f'Cambio de contraseña',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                resource_type='user',
                resource_id=current_user.id
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Su contraseña ha sido actualizada.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('La contraseña actual es incorrecta.', 'error')
    
    return render_template('auth/change_password.html', form=form)