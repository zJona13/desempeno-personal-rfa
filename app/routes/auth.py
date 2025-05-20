# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
# from tools.jwt_utils import generar_token # Si decides volver a JWT en sesión

auth_bp = Blueprint('auth', __name__, url_prefix='/auth') # Puedes omitir url_prefix si prefieres /login y /register directos

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'): # Usamos user_id para verificar sesión activa
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        correo = request.form.get('email')
        contrasena = request.form.get('password')
        
        nombre_val = correo # Para pre-rellenar

        if not correo or not contrasena:
            flash('Correo y contraseña son requeridos.', 'error')
            return render_template('login.html', email=nombre_val)

        usuario_data = User.find_by_email(correo)

        if usuario_data and usuario_data['vigencia'] == 1 and User.verify_user_password(usuario_data['contrasena'], contrasena):
            session['user_id'] = usuario_data['idUsuario']
            session['user_name'] = usuario_data['nombre']
            session['user_role_id'] = usuario_data['idTipoUsu']
            session.permanent = True # Para que use PERMANENT_SESSION_LIFETIME

            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('main.dashboard')) # 'main.dashboard' porque dashboard estará en main_bp
        else:
            flash('Credenciales inválidas o usuario inactivo.', 'error')
            return render_template('login.html', email=nombre_val)

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.dashboard'))

    nombre_val = request.form.get('name', '')
    correo_val = request.form.get('email', '')

    if request.method == 'POST':
        nombre = request.form.get('name')
        correo = request.form.get('email')
        contrasena = request.form.get('password')
        confirm_contrasena = request.form.get('confirmPassword')

        nombre_val = nombre
        correo_val = correo

        if not all([nombre, correo, contrasena, confirm_contrasena]):
            flash('Todos los campos son requeridos.', 'error')
            return render_template('register.html', name=nombre_val, email=correo_val)

        if contrasena != confirm_contrasena:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html', name=nombre_val, email=correo_val)
        
        success, message = User.create(nombre, correo, contrasena)

        if success:
            flash(message, 'success')
            return redirect(url_for('auth.login')) # Redirige a la ruta de login del blueprint 'auth'
        else:
            flash(message, 'error')
            return render_template('register.html', name=nombre_val, email=correo_val)
            
    return render_template('register.html', name=nombre_val, email=correo_val)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))