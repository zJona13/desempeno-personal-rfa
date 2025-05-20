<<<<<<< HEAD
from flask import Flask, render_template
from routes.route_sesion import ws_sesion

app = Flask(__name__)
app.register_blueprint(ws_sesion)
=======
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from config import Config
from conexionBD import Conexion
from tools.security import hash_password, verify_password
from tools.jwt_utils import generar_token # No usaremos jwt_required directamente en app.py para proteger plantillas inicialmente
                                         # sino que manejaremos la sesión. jwt_required es más para APIs.
import datetime # Para el contexto de 'now' en la sidebar

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30) # O el tiempo que consideres

# Datos de navegación (ejemplo, esto podría venir de la BD o un archivo de config)
def get_nav_items(user_role_id=None):
    # Todos los usuarios ven Login si no están logueados
    if not session.get('user_token'):
        return [] # O quizás un item para login

    # Base nav_items
    nav_items_all = [
        {"href": "/dashboard", "title": "Dashboard", "icon_svg_name": "home"},
        {"href": "/self_evaluation", "title": "Autoevaluación", "icon_svg_name": "user-square-2"},
        {"href": "/student_evaluation", "title": "Evaluar Docentes", "icon_svg_name": "clipboard-list"}, # Estudiante
        {"href": "/checklist_evaluation", "title": "Lista de Cotejo", "icon_svg_name": "check-square"}, # Evaluador/Admin
        {"href": "/results", "title": "Resultados", "icon_svg_name": "bar-chart-4"},
        {"href": "/incidents", "title": "Incidencias", "icon_svg_name": "alert-circle"},
        # Admin specific
        {"href": "/validation", "title": "Validación", "icon_svg_name": "shield-check"},
        {"href": "/roles", "title": "Roles y Permisos", "icon_svg_name": "users"},
    ]
    
    # Lógica para filtrar items basado en user_role_id
    # Esto es un ejemplo, necesitarás mapear idTipoUsu a roles y permisos más detallados
    # idTipoUsu: 1=Admin, 2=Docente, 3=Evaluador, 4=Estudiante, 5=Developer (según tablas_bd.sql)
    if user_role_id == 1 or user_role_id == 5: # Admin o Developer
        return nav_items_all
    elif user_role_id == 2: # Docente
        return [
            {"href": "/dashboard", "title": "Dashboard", "icon_svg_name": "home"},
            {"href": "/self_evaluation", "title": "Autoevaluación", "icon_svg_name": "user-square-2"},
            {"href": "/results", "title": "Resultados", "icon_svg_name": "bar-chart-4"},
            {"href": "/incidents", "title": "Incidencias", "icon_svg_name": "alert-circle"},
        ]
    elif user_role_id == 4: # Estudiante
        return [
            {"href": "/dashboard", "title": "Dashboard", "icon_svg_name": "home"},
            {"href": "/student_evaluation", "title": "Evaluar Docentes", "icon_svg_name": "clipboard-list"},
            {"href": "/incidents", "title": "Incidencias", "icon_svg_name": "alert-circle"},
        ]
    # Añadir más roles según sea necesario
    return [nav_items_all[0]] # Por defecto, solo dashboard si el rol no está mapeado

def get_user_role_display(user_role_id=None):
    if not user_role_id:
        return "Invitado"
    try:
        db = Conexion().open
        cursor = db.cursor()
        cursor.execute("SELECT nombre FROM TIPO_USUARIO WHERE idTipoUsu = %s", (user_role_id,))
        role_name = cursor.fetchone()
        cursor.close()
        db.close()
        return role_name[0] if role_name else "Desconocido"
    except Exception as e:
        print(f"Error fetching role display: {e}")
        return "Error Rol"

@app.context_processor
def inject_global_vars():
    user_token = session.get('user_token')
    user_role_id = session.get('user_role_id')
    nav_items = get_nav_items(user_role_id)
    current_user_role_display = get_user_role_display(user_role_id)
    return dict(
        nav_items=nav_items,
        current_user_role_display=current_user_role_display,
        now=datetime.datetime.utcnow(), # Para el copyright del año en sidebar
        show_sidebar_header= (user_token is not None) # Mostrar sidebar y header solo si está logueado
    )
>>>>>>> 9ddca798e95b8c8a5a3b83eef9920a93ecd46f0d

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_token'): # Si ya está logueado, redirigir al dashboard
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        correo = request.form['email']
        contrasena = request.form['password']

        if not correo or not contrasena:
            flash('Correo y contraseña son requeridos.', 'error')
            return render_template('login.html', email=correo)

        try:
            db = Conexion().open
            cursor = db.cursor(dictionary=True) # Usar dictionary=True para acceder por nombre de columna
            cursor.execute("SELECT idUsuario, nombre, contrasena, idTipoUsu, vigencia FROM USUARIO WHERE correo = %s", (correo,))
            usuario_data = cursor.fetchone()
            cursor.close()
            db.close()

            if usuario_data and usuario_data['vigencia'] == 1 and verify_password(usuario_data['contrasena'], contrasena):
                # Credenciales válidas
                payload = {
                    'idUsuario': usuario_data['idUsuario'],
                    'nombre': usuario_data['nombre'],
                    'idTipoUsu': usuario_data['idTipoUsu'],
                    # 'exp' se añade en generar_token
                }
                # El tiempo de expiración del token JWT ahora está en segundos
                token = generar_token(payload, exp_seconds=Config.DB_PORT) # Usamos DB_PORT (3306) como ejemplo de segundos, cámbialo a algo razonable (ej. 1800 para 30 mins)

                session['user_token'] = token
                session['user_id'] = usuario_data['idUsuario']
                session['user_name'] = usuario_data['nombre']
                session['user_role_id'] = usuario_data['idTipoUsu']
                session.permanent = True # Para que use PERMANENT_SESSION_LIFETIME

                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales inválidas o usuario inactivo.', 'error')
                return render_template('login.html', email=correo)

        except Exception as e:
            flash(f'Error durante el inicio de sesión: {str(e)}', 'error')
            print(f"Error en login: {e}") # Para depuración en consola
            return render_template('login.html', email=correo)

    return render_template('login.html')


<<<<<<< HEAD
=======
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_token'): # Si ya está logueado, redirigir al dashboard
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nombre = request.form.get('name')
        correo = request.form.get('email')
        contrasena = request.form.get('password')
        confirm_contrasena = request.form.get('confirmPassword')

        if not all([nombre, correo, contrasena, confirm_contrasena]):
            flash('Todos los campos son requeridos.', 'error')
            # AQUÍ FALTA EL RETURN render_template
            return render_template('register.html', name=nombre, email=correo, _block='content_without_sidebar') # Asegúrate de pasar el bloque correcto

        if contrasena != confirm_contrasena:
            flash('Las contraseñas no coinciden.', 'error')
            # AQUÍ FALTA EL RETURN render_template
            return render_template('register.html', name=nombre, email=correo, _block='content_without_sidebar') # Asegúrate de pasar el bloque correcto

        # Verificar si el correo ya existe
        try:
            db = Conexion().open # Mover la apertura de la conexión aquí
            cursor = db.cursor()
            cursor.execute("SELECT idUsuario FROM USUARIO WHERE correo = %s", (correo,))
            if cursor.fetchone():
                flash('El correo electrónico ya está registrado.', 'error')
                cursor.close()
                db.close()
                # AQUÍ FALTA EL RETURN render_template
                return render_template('register.html', name=nombre, email=correo, _block='content_without_sidebar') # Asegúrate de pasar el bloque correcto
            
            hashed_pass = hash_password(contrasena)
            id_tipo_usuario_default = 4 
            vigencia_default = 1

            cursor.execute(
                "INSERT INTO USUARIO (nombre, correo, contrasena, vigencia, idTipoUsu) VALUES (%s, %s, %s, %s, %s)",
                (nombre, correo, hashed_pass, vigencia_default, id_tipo_usuario_default)
            )
            db.commit()
            # No cierres el cursor y la db aquí si los vas a usar en finally
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login')) # Esto parece correcto
        except Exception as e:
            # db.rollback() # Descomentar si tu conexión/ORM lo soporta y es necesario
            if 'db' in locals() and db.is_connected(): # Solo si db se inicializó
                 db.rollback() # Es buena práctica hacer rollback aquí
            flash(f'Error durante el registro: {str(e)}', 'error')
            print(f"Error en register (POST): {e}") # Imprime el error para depuración
            # AQUÍ FALTA EL RETURN render_template
            return render_template('register.html', name=nombre, email=correo, _block='content_without_sidebar') # Asegúrate de pasar el bloque correcto
        finally:
            if 'db' in locals() and db.is_connected(): # Verificar si db fue inicializada y está conectada
                if 'cursor' in locals() and cursor: # Verificar si cursor fue inicializado
                    cursor.close()
                db.close()
                
    # Para el método GET
    return render_template('register.html', _block='content_without_sidebar') # Asegúrate de pasar el bloque correcto

@app.route('/dashboard')
def dashboard():
    if not session.get('user_token'):
        flash('Debes iniciar sesión para acceder a esta página.', 'info')
        return redirect(url_for('login'))

    # Aquí iría la lógica para obtener los datos del dashboard
    # Ejemplo de datos para las tarjetas de estadísticas y módulos
    user_name = session.get('user_name', 'Usuario')
    greeting = "Hola" # Podrías personalizar el saludo según la hora

    stats = {
        "evaluaciones_pendientes": 5, # Ejemplo
        "trend_evaluaciones": {"is_positive": True, "value": 10}, # Ejemplo
        "incidencias_activas": 2, # Ejemplo
        "trend_incidencias": {"is_positive": False, "value": 5}, # Ejemplo
        "validaciones_pendientes": 3, # Ejemplo
        "total_resultados": 150, # Ejemplo
        "trend_resultados": {"is_positive": True, "value": 12} # Ejemplo
    }
    
    # Módulos basados en el rol (ejemplo simplificado)
    user_role_id = session.get('user_role_id')
    modules = []
    if user_role_id == 1 or user_role_id == 5: # Admin o Developer
        modules = [
            {"title": "Autoevaluación Personal", "description": "Complete o revise su autoevaluación.", "href": url_for('self_evaluation'), "icon_svg_name": "user-square-2", "color": "bg-blue-100 text-blue-600 dark:bg-blue-700 dark:text-blue-200"},
            {"title": "Evaluar con Lista de Cotejo", "description": "Realice evaluaciones usando criterios definidos.", "href": url_for('checklist_evaluation'), "icon_svg_name": "clipboard-list", "color": "bg-green-100 text-green-600 dark:bg-green-700 dark:text-green-200"},
            {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
            {"title": "Validación de Evaluaciones", "description": "Revise y valide evaluaciones.", "href": url_for('validation'), "icon_svg_name": "shield-check", "color": "bg-purple-100 text-purple-600 dark:bg-purple-700 dark:text-purple-200"},
            {"title": "Administrar Roles", "description": "Gestione roles y permisos de usuarios.", "href": url_for('roles'), "icon_svg_name": "users", "color": "bg-red-100 text-red-600 dark:bg-red-700 dark:text-red-200"},
            {"title": "Ver Resultados", "description": "Consulte los resultados de las evaluaciones.", "href": url_for('results'), "icon_svg_name": "bar-chart-4", "color": "bg-indigo-100 text-indigo-600 dark:bg-indigo-700 dark:text-indigo-200"}
        ]
    elif user_role_id == 2: # Docente
         modules = [
            {"title": "Autoevaluación Personal", "description": "Complete o revise su autoevaluación.", "href": url_for('self_evaluation'), "icon_svg_name": "user-square-2", "color": "bg-blue-100 text-blue-600 dark:bg-blue-700 dark:text-blue-200"},
            {"title": "Ver Resultados", "description": "Consulte sus resultados de evaluaciones.", "href": url_for('results'), "icon_svg_name": "bar-chart-4", "color": "bg-indigo-100 text-indigo-600 dark:bg-indigo-700 dark:text-indigo-200"},
            {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
        ]
    elif user_role_id == 4: # Estudiante
        modules = [
             {"title": "Evaluación Docente", "description": "Evalúe el desempeño de sus docentes.", "href": url_for('student_evaluation'), "icon_svg_name": "clipboard-list", "color": "bg-green-100 text-green-600 dark:bg-green-700 dark:text-green-200"},
             {"title": "Gestión de Incidencias", "description": "Registre y siga las incidencias.", "href": url_for('incidents'), "icon_svg_name": "alert-circle", "color": "bg-yellow-100 text-yellow-600 dark:bg-yellow-700 dark:text-yellow-200"},
        ]


    return render_template('dashboard.html', greeting=greeting, user_name=user_name, stats=stats, modules=modules)

@app.route('/logout')
def logout():
    session.clear() # Limpia toda la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

# Rutas de ejemplo para las demás páginas (solo para que los enlaces del sidebar funcionen)
# Deberás implementar la lógica y protección para cada una
@app.route('/self_evaluation')
def self_evaluation():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data for self-evaluation list page (not form)
    evaluations = [
        {"id": 1, "title": "Autoevaluación Semestral 2025-I", "status": "active", "status_text": "Pendiente", "status_icon": "clock", "status_bg_color": "bg-yellow-100", "status_text_color":"text-yellow-700", "due_date": "2025-06-15", "criteria_count": 25, "estimated_time_minutes": 30, "action_button_text": "Iniciar Evaluación", "action_button_variant":"primary", "action_url_param": 1},
        {"id": 2, "title": "Autoevaluación Anual 2024", "status": "completed", "status_text": "Completado", "status_icon": "check-circle-2", "status_bg_color": "bg-green-100", "status_text_color":"text-green-700", "completed_date": "2024-12-01", "criteria_count": 20, "score": "92%", "action_button_text": "Ver Resultados", "action_button_variant":"outline", "action_url_param": 2},
    ]
    # evaluation_data es para el formulario, show_form para controlar qué se muestra
    # Para la lista, show_form sería False. Si se accede a /self_evaluation?evaluation_id=1, show_form sería True.
    show_form_param = request.args.get('evaluation_id') # En la plantilla real, esto sería `request.args.get('evaluation_id')`
    show_form = bool(show_form_param) 
    evaluation_data = None
    if show_form: # Lógica para cargar datos del formulario si se está editando/viendo uno específico
        evaluation_data = {
            "title": "Autoevaluación Semestral 2025-I",
            "criteria": [
                {"id": 1, "category": "Planificación Curricular", "text": "Elabora el sílabo considerando el perfil del egresado.", "value": None, "comment": ""},
                {"id": 2, "category": "Planificación Curricular", "text": "Presenta el sílabo a los estudiantes al inicio del semestre.", "value": None, "comment": ""},
                {"id": 3, "category": "Proceso de Enseñanza-Aprendizaje", "text": "Utiliza estrategias de enseñanza activas y participativas.", "value": None, "comment": ""},
            ]
        }


    return render_template('self-evaluation.html', evaluations=evaluations, show_form=show_form, evaluation_data=evaluation_data)

@app.route('/student_evaluation')
def student_evaluation():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data
    evaluations_pending = [
        {"id": 1, "subject_name": "Matemática Aplicada I", "teacher_name": "Dr. Alan Turing", "section": "A"},
        {"id": 2, "subject_name": "Desarrollo Web Fullstack", "teacher_name": "Ing. Ada Lovelace", "section": "B"},
    ]
    return render_template('student-evaluation.html', evaluations_pending=evaluations_pending)

@app.route('/checklist_evaluation')
def checklist_evaluation():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data
    pending_evaluations = [
        {"id": 101, "name": "Carlos Santana", "role": "Docente Contratado", "department": "Ciencias Básicas"},
    ]
    completed_evaluations = [
        {"id": 201, "name": "Luisa Pérez", "role": "Docente Principal", "department": "Ingeniería", "score": "88%", "completed_date": "2025-05-10"},
    ]
    return render_template('checklist-evaluation.html', pending_evaluations=pending_evaluations, completed_evaluations=completed_evaluations)

@app.route('/results')
def results():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data for summary
    summary = {
        "pedagogico": {"score_percent": 85, "text_color": "text-green-600"},
        "academico": {"score_percent": 90, "text_color": "text-green-600"},
        "gestion": {"score_percent": 75, "text_color": "text-yellow-600"},
        "global": {"score_percent": 83, "text_color": "text-green-600"}
    }
    return render_template('results.html', summary=summary)

@app.route('/incidents')
def incidents():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data
    incidents_data = [
        {"id": 1, "title": "Error al cargar notas", "reported_date": "2025-05-18", "type": "Sistema", "status": "En proceso", "description_summary": "Los estudiantes no pueden ver sus calificaciones...", "status_color_class": "bg-yellow-500 text-white"},
        {"id": 2, "title": "Aula sin proyector", "reported_date": "2025-05-15", "type": "Infraestructura", "status": "Resuelto", "description_summary": "Se solicitó un proyector para el aula C-102.", "status_color_class": "bg-green-100 text-green-700"},
    ]
    return render_template('incidents.html', incidents=incidents_data)

@app.route('/validation')
def validation():
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data
    autoevaluaciones_pendientes = [
        {"id": 301, "name": "Ana Torres", "type": "Autoevaluación Docente", "role_department": "Docente - Idiomas", "submitted_date": "2025-05-20"},
    ]
    listas_cotejo_pendientes = []
    validaciones_recientes = [
        {"id": 401, "name": "Pedro Castillo", "type": "Autoevaluación", "validated_date": "2025-05-19", "status": "Aprobado", "status_icon": "check-circle-2", "status_color_class": "text-green-600 bg-green-100", "score": "90%"},
    ]
    return render_template('validation.html', 
                           autoevaluaciones_pendientes=autoevaluaciones_pendientes, 
                           listas_cotejo_pendientes=listas_cotejo_pendientes, 
                           validaciones_recientes=validaciones_recientes)

@app.route('/roles') # /admin/manage_roles
def roles(): # Cambiado de manage_roles a roles para coincidir con url_for
    if not session.get('user_token'): return redirect(url_for('login'))
    # Dummy data
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

    # Para la matriz de permisos (simplificado)
    all_roles_for_matrix = roles_data 
    permissions_matrix = [
        {"id": "mod1", "module": "Gestión de Usuarios", "actions": ["crear", "editar", "eliminar", "ver"]},
        {"id": "mod2", "module": "Evaluaciones", "actions": ["realizar_autoevaluacion", "evaluar_pares", "validar_evaluacion"]},
    ]
    
    # Función dummy para simular la obtención de permisos
    # En una app real, esto consultaría la BD o una estructura de permisos
    def get_role_permission(role_name, module_name, action_name):
        # Ejemplo: Admin tiene todos los permisos
        if role_name == "Administrador":
            return True
        if role_name == "Docente" and module_name == "Evaluaciones" and action_name == "realizar_autoevaluacion":
            return True
        # ... más lógica ...
        return False

    return render_template('roles.html', 
                           active_tab=active_tab, 
                           search_query=search_query,
                           roles=roles_data, 
                           users=users_data,
                           all_roles_for_matrix=all_roles_for_matrix,
                           permissions_matrix=permissions_matrix,
                           get_role_permission=get_role_permission, # Pasar la función al template
                           validation_errors_for_dialog=None) # Para el modal de nuevo rol


>>>>>>> 9ddca798e95b8c8a5a3b83eef9920a93ecd46f0d
#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=8080, debug=True, host='0.0.0.0')