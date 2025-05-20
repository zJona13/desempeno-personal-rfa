# app/routes/admin.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.criterion import Criterion
from app.models.collaborator import CollaboratorType, ContractType
from app.models.collaborator import Collaborator, CollaboratorType, ContractType # Actualizar importación
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para proteger rutas de administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Debes iniciar sesión para acceder a esta página.', 'info')
            return redirect(url_for('auth.login'))
        # Asumimos que user_role_id = 1 es Administrador
        if session.get('user_role_id') != 1 and session.get('user_role_id') != 5: # 5 para Developer
            flash('No tienes permisos para acceder a esta sección.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/criteria', methods=['GET', 'POST'])
@admin_required
def manage_criteria():
    if request.method == 'POST':
        action = request.form.get('action')
        criterion_id = request.form.get('criterion_id')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        # El valor de 'valor' podría ser None o string vacío si no se ingresa, convertir a int o None
        try:
            valor_str = request.form.get('valor')
            valor = int(valor_str) if valor_str and valor_str.isdigit() else None
        except ValueError:
            valor = None # O manejar el error como prefieras

        vigencia = 1 if request.form.get('vigencia') == 'on' else 0 # Checkbox

        if action == 'create':
            if not nombre:
                flash('El nombre del criterio es requerido.', 'error')
            else:
                success, message = Criterion.create(nombre, descripcion, valor, vigencia)
                if success:
                    flash(message, 'success')
                else:
                    flash(message, 'error')
        
        elif action == 'update':
            if not criterion_id or not nombre:
                 flash('Faltan datos para actualizar el criterio.', 'error')
            else:
                success, message = Criterion.update(criterion_id, nombre, descripcion, valor, vigencia)
                if success:
                    flash(message, 'success')
                else:
                    flash(message, 'error')
        return redirect(url_for('admin.manage_criteria'))

    # Para GET request o si el POST no redirige (ej. error de validación que vuelve a mostrar el form)
    criteria_list = Criterion.get_all()
    return render_template('admin/manage_criteria.html', criteria_list=criteria_list, criterion_to_edit=None)

@admin_bp.route('/criteria/edit/<int:criterion_id>', methods=['GET'])
@admin_required
def edit_criterion_form(criterion_id):
    criterion_to_edit = Criterion.get_by_id(criterion_id)
    if not criterion_to_edit:
        flash('Criterio no encontrado.', 'error')
        return redirect(url_for('admin.manage_criteria'))
    
    criteria_list = Criterion.get_all() # Para mostrar la lista en la misma página
    return render_template('admin/manage_criteria.html', criteria_list=criteria_list, criterion_to_edit=criterion_to_edit)

@admin_bp.route('/criteria/delete/<int:criterion_id>', methods=['POST']) # Usar POST para acciones destructivas
@admin_required
def delete_criterion(criterion_id):
    success, message = Criterion.delete(criterion_id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    return redirect(url_for('admin.manage_criteria'))

@admin_bp.route('/collaborator-types', methods=['GET', 'POST'])
@admin_required
def manage_collaborator_types():
    if request.method == 'POST':
        action = request.form.get('action')
        type_id = request.form.get('type_id')
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre del tipo es requerido.', 'error')
        else:
            if action == 'create':
                success, message = CollaboratorType.create(nombre)
                flash(message, 'success' if success else 'error')
            elif action == 'update' and type_id:
                success, message = CollaboratorType.update(type_id, nombre)
                flash(message, 'success' if success else 'error')
        return redirect(url_for('admin.manage_collaborator_types'))

    types_list = CollaboratorType.get_all()
    return render_template('admin/manage_collaborator_types.html', types_list=types_list, type_to_edit=None)

@admin_bp.route('/collaborator-types/edit/<int:type_id>', methods=['GET'])
@admin_required
def edit_collaborator_type_form(type_id):
    type_to_edit = CollaboratorType.get_by_id(type_id)
    if not type_to_edit:
        flash('Tipo de colaborador no encontrado.', 'error')
        return redirect(url_for('admin.manage_collaborator_types'))
    
    types_list = CollaboratorType.get_all()
    return render_template('admin/manage_collaborator_types.html', types_list=types_list, type_to_edit=type_to_edit)

@admin_bp.route('/collaborator-types/delete/<int:type_id>', methods=['POST'])
@admin_required
def delete_collaborator_type(type_id):
    success, message = CollaboratorType.delete(type_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin.manage_collaborator_types'))

# --- NUEVAS RUTAS PARA TIPOS DE CONTRATO ---
@admin_bp.route('/contract-types', methods=['GET', 'POST'])
@admin_required
def manage_contract_types():
    if request.method == 'POST':
        action = request.form.get('action')
        type_id = request.form.get('type_id')
        nombre = request.form.get('nombre')

        if not nombre:
            flash('El nombre del tipo es requerido.', 'error')
        else:
            if action == 'create':
                success, message = ContractType.create(nombre)
                flash(message, 'success' if success else 'error')
            elif action == 'update' and type_id:
                success, message = ContractType.update(type_id, nombre)
                flash(message, 'success' if success else 'error')
        return redirect(url_for('admin.manage_contract_types'))

    types_list = ContractType.get_all()
    return render_template('admin/manage_contract_types.html', types_list=types_list, type_to_edit=None)

@admin_bp.route('/contract-types/edit/<int:type_id>', methods=['GET'])
@admin_required
def edit_contract_type_form(type_id):
    type_to_edit = ContractType.get_by_id(type_id)
    if not type_to_edit:
        flash('Tipo de contrato no encontrado.', 'error')
        return redirect(url_for('admin.manage_contract_types'))
    
    types_list = ContractType.get_all()
    return render_template('admin/manage_contract_types.html', types_list=types_list, type_to_edit=type_to_edit)

@admin_bp.route('/contract-types/delete/<int:type_id>', methods=['POST'])
@admin_required
def delete_contract_type(type_id):
    success, message = ContractType.delete(type_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin.manage_contract_types'))

@admin_bp.route('/collaborators', methods=['GET'])
@admin_required
def manage_collaborators():
    collaborators_list = Collaborator.get_all_with_details()
    return render_template('admin/manage_collaborators.html', collaborators_list=collaborators_list)

@admin_bp.route('/collaborators/new', methods=['GET', 'POST'])
@admin_required
def new_collaborator():
    if request.method == 'POST':
        # Recoger datos del formulario del colaborador
        nombres = request.form.get('nombres')
        ape_pat = request.form.get('apePat')
        ape_mat = request.form.get('apeMat')
        try:
            fecha_nac_str = request.form.get('fechaNacimiento')
            fecha_nac = datetime.datetime.strptime(fecha_nac_str, '%Y-%m-%d').date() if fecha_nac_str else None
        except ValueError:
            flash('Formato de fecha de nacimiento inválido. Use YYYY-MM-DD.', 'error')
            fecha_nac = None # o redirigir con error
        
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        dni = request.form.get('dni')
        estado_colab = int(request.form.get('estado_colaborador', 1)) # Default a 1 (activo)
        id_tipo_colab = request.form.get('idTipoColab')

        # Recoger datos del formulario del contrato
        try:
            fecha_inicio_contrato_str = request.form.get('fechaInicioContrato')
            fecha_inicio_contrato = datetime.datetime.strptime(fecha_inicio_contrato_str, '%Y-%m-%d').date() if fecha_inicio_contrato_str else None
            fecha_fin_contrato_str = request.form.get('fechaFinContrato')
            fecha_fin_contrato = datetime.datetime.strptime(fecha_fin_contrato_str, '%Y-%m-%d').date() if fecha_fin_contrato_str else None
        except ValueError:
            flash('Formato de fecha de contrato inválido. Use YYYY-MM-DD.', 'error')
            # Recargar el formulario con los datos y el error
            collaborator_types = CollaboratorType.get_all()
            contract_types = ContractType.get_all()
            return render_template('admin/collaborator_form.html', 
                                   collaborator_types=collaborator_types, 
                                   contract_types=contract_types, 
                                   form_data=request.form,
                                   form_title="Nuevo Colaborador")


        estado_contrato = int(request.form.get('estado_contrato', 1)) # Default a 1 (activo)
        modalidad_contrato = request.form.get('modalidadContrato')
        id_tipo_contrato = request.form.get('idTipoContrato')
        
        # id_usuario_vinculado = request.form.get('idUsuario') # Si lo implementas

        # Validaciones básicas (puedes añadir más)
        if not all([nombres, ape_pat, dni, id_tipo_colab, fecha_inicio_contrato, modalidad_contrato, id_tipo_contrato]):
            flash('Campos requeridos del colaborador o contrato están vacíos.', 'error')
        else:
            success, message = Collaborator.create(
                nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab,
                fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, modalidad_contrato, id_tipo_contrato
                # , id_usuario_vinculado # si lo implementas
            )
            flash(message, 'success' if success else 'error')
            if success:
                return redirect(url_for('admin.manage_collaborators'))
        
    # Para GET o si el POST falla y necesita recargar el formulario
    collaborator_types = CollaboratorType.get_all()
    contract_types = ContractType.get_all()
    # Podrías querer pasar usuarios para vincular:
    # from app.models.user import User
    # users_list = User.get_all_active_users() # Necesitarías un método así en User model
    return render_template('admin/collaborator_form.html', 
                           collaborator_types=collaborator_types, 
                           contract_types=contract_types, 
                           # users_list=users_list, 
                           form_data=request.form if request.method == 'POST' else {}, # Para repoblar en error
                           form_title="Nuevo Colaborador")


@admin_bp.route('/collaborators/edit/<int:collaborator_id>', methods=['GET', 'POST'])
@admin_required
def edit_collaborator(collaborator_id):
    collaborator_data = Collaborator.get_by_id_with_details(collaborator_id)
    if not collaborator_data:
        flash('Colaborador no encontrado.', 'error')
        return redirect(url_for('admin.manage_collaborators'))

    if request.method == 'POST':
        nombres = request.form.get('nombres')
        ape_pat = request.form.get('apePat')
        ape_mat = request.form.get('apeMat')
        try:
            fecha_nac_str = request.form.get('fechaNacimiento')
            fecha_nac = datetime.datetime.strptime(fecha_nac_str, '%Y-%m-%d').date() if fecha_nac_str else None
        except ValueError:
             flash('Formato de fecha de nacimiento inválido. Use YYYY-MM-DD.', 'error')
             fecha_nac = collaborator_data['fechaNacimiento'] # Mantener valor anterior

        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        dni = request.form.get('dni')
        estado_colab = int(request.form.get('estado_colaborador', collaborator_data['estado_colaborador']))
        id_tipo_colab = request.form.get('idTipoColab')

        contract_id = collaborator_data['idContrato'] # El ID del contrato no debería cambiar, se actualiza
        try:
            fecha_inicio_contrato_str = request.form.get('fechaInicioContrato')
            fecha_inicio_contrato = datetime.datetime.strptime(fecha_inicio_contrato_str, '%Y-%m-%d').date() if fecha_inicio_contrato_str else None
            fecha_fin_contrato_str = request.form.get('fechaFinContrato')
            fecha_fin_contrato = datetime.datetime.strptime(fecha_fin_contrato_str, '%Y-%m-%d').date() if fecha_fin_contrato_str else None
        except ValueError:
            flash('Formato de fecha de contrato inválido. Use YYYY-MM-DD.', 'error')
            # Mantener valores anteriores si el formato es incorrecto
            fecha_inicio_contrato = collaborator_data['fechaInicio']
            fecha_fin_contrato = collaborator_data['fechaFin']
            
        estado_contrato = int(request.form.get('estado_contrato', collaborator_data['estado_contrato']))
        modalidad_contrato = request.form.get('modalidadContrato')
        id_tipo_contrato = request.form.get('idTipoContrato')
        # id_usuario_vinculado = request.form.get('idUsuario') # si lo implementas

        if not all([nombres, ape_pat, dni, id_tipo_colab, contract_id, fecha_inicio_contrato, modalidad_contrato, id_tipo_contrato]):
            flash('Campos requeridos del colaborador o contrato están vacíos.', 'error')
        else:
            success, message = Collaborator.update(
                collaborator_id, nombres, ape_pat, ape_mat, fecha_nac, direccion, telefono, dni, estado_colab, id_tipo_colab,
                contract_id, fecha_inicio_contrato, fecha_fin_contrato, estado_contrato, modalidad_contrato, id_tipo_contrato
                # , id_usuario_vinculado # si lo implementas
            )
            flash(message, 'success' if success else 'error')
            if success:
                return redirect(url_for('admin.manage_collaborators'))
        
        # Si hay error o es GET, se recarga el form. Volver a obtener los datos para pasar al template.
        # Es importante repoblar `collaborator_data` con lo que vino del formulario si hubo un error de validación
        # para que el usuario no pierda sus cambios.
        # Esto se puede hacer construyendo un diccionario con request.form o pasando request.form directamente.

    collaborator_types = CollaboratorType.get_all()
    contract_types = ContractType.get_all()
    # users_list = User.get_all_active_users() # Si implementas vinculación

    # Si es GET, collaborator_data es de la BD. Si es POST con error, debería ser de request.form.
    # Para simplificar, siempre pasamos collaborator_data (de la BD) para precargar,
    # y el usuario ve los mensajes flash para errores.
    return render_template('admin/collaborator_form.html', 
                           collaborator_types=collaborator_types, 
                           contract_types=contract_types,
                           # users_list=users_list, 
                           collaborator=collaborator_data, # Datos del colaborador y su contrato para el formulario
                           form_title="Editar Colaborador")


@admin_bp.route('/collaborators/delete/<int:collaborator_id>', methods=['POST'])
@admin_required
def delete_collaborator(collaborator_id):
    # Actualmente el modelo solo inactiva, no elimina.
    success, message = Collaborator.delete(collaborator_id) 
    flash(message, 'success' if success else 'error')
    return redirect(url_for('admin.manage_collaborators'))


# Aquí irán las rutas para Colaboradores, Tipos de Contrato, etc.
# Por ejemplo:
# @admin_bp.route('/collaborators')
# @admin_required
# def manage_collaborators():
#     # ... lógica ...
#     return render_template('admin/manage_collaborators.html')