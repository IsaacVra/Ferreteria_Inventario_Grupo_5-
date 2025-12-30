from flask import Blueprint, request, jsonify, session
from database.models import Usuario
from database.database import db
from utils.decorators import login_required, roles_required
from utils.security import hash_password

# Crear un Blueprint para las rutas de usuarios
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['GET'])
@login_required
@roles_required('ADMIN', 'GERENTE')
def get_users():
    """Obtiene todos los usuarios activos."""
    try:
        query = """
        SELECT u.id_usuario, u.usuario_login, u.nombres, u.apellidos, u.email, 
               u.estado, tu.nombre_tipo as rol, u.telefono, u.cedula,
               u.fecha_creacion, u.fecha_actualizacion
        FROM USUARIO u
        JOIN TIPO_USUARIO tu ON u.id_tipo_usuario = tu.id_tipo_usuario
        WHERE u.estado = 'ACTIVO'
        ORDER BY u.nombres
        """
        
        users = db.execute_query(query)
        return jsonify({'success': True, 'data': users})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@users_bp.route('', methods=['POST'])
@login_required
@roles_required('ADMIN')
def create_user():
    """Crea un nuevo usuario."""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombres', 'apellidos', 'usuario_login', 'clave', 'email', 'id_tipo_usuario']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'El campo {field} es requerido'}), 400
        
        # Verificar si el usuario o email ya existen
        check_query = """
        SELECT id_usuario 
        FROM USUARIO 
        WHERE (usuario_login = %s OR email = %s) AND estado = 'ACTIVO'
        """
        existing = db.execute_query(check_query, (data['usuario_login'], data['email']))
        
        if existing:
            return jsonify({
                'success': False, 
                'error': 'El nombre de usuario o correo electrónico ya está en uso'
            }), 400
        
        # Hashear la contraseña
        hashed_password = hash_password(data['clave'])
        
        # Crear el usuario
        user_data = {
            'nombres': data['nombres'],
            'apellidos': data['apellidos'],
            'usuario_login': data['usuario_login'],
            'clave_hash': hashed_password,
            'email': data['email'],
            'telefono': data.get('telefono', ''),
            'id_tipo_usuario': data['id_tipo_usuario'],
            'cedula': data.get('cedula', '')
        }
        
        result = Usuario.create(user_data)
        
        if result and 'lastrowid' in result:
            # Obtener el usuario creado
            new_user = Usuario.get_by_id(result['lastrowid'])
            return jsonify({
                'success': True, 
                'message': 'Usuario creado correctamente',
                'data': new_user
            }), 201
        else:
            return jsonify({
                'success': False, 
                'error': 'Error al crear el usuario'
            }), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
@roles_required('ADMIN')
def update_user(user_id):
    """Actualiza un usuario existente."""
    try:
        data = request.get_json()
        
        # Validar que el usuario exista
        user = Usuario.get_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Verificar si el email ya está en uso por otro usuario
        if 'email' in data:
            check_query = """
            SELECT id_usuario 
            FROM USUARIO 
            WHERE email = %s AND id_usuario != %s AND estado = 'ACTIVO'
            """
            existing = db.execute_query(check_query, (data['email'], user_id))
            if existing:
                return jsonify({
                    'success': False, 
                    'error': 'El correo electrónico ya está en uso por otro usuario'
                }), 400
        
        # Actualizar el usuario
        update_data = {
            'nombres': data.get('nombres', user['nombres']),
            'apellidos': data.get('apellidos', user['apellidos']),
            'email': data.get('email', user['email']),
            'telefono': data.get('telefono', user.get('telefono', '')),
            'id_tipo_usuario': data.get('id_tipo_usuario', user['id_tipo_usuario']),
            'cedula': data.get('cedula', user.get('cedula', ''))
        }
        
        # Si se proporciona una nueva contraseña, hashearla
        if 'clave' in data and data['clave']:
                        update_data['clave_hash'] = hash_password(data['clave'])
        
        result = Usuario.update(user_id, update_data)
        
        if result and result.get('affected_rows', 0) > 0:
            updated_user = Usuario.get_by_id(user_id)
            return jsonify({
                'success': True, 
                'message': 'Usuario actualizado correctamente',
                'data': updated_user
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'No se pudo actualizar el usuario'
            }), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@roles_required('ADMIN')
def delete_user(user_id):
    """Elimina un usuario (eliminación lógica)."""
    try:
        # Verificar que el usuario no se esté eliminando a sí mismo
        if session.get('user_id') == user_id:
            return jsonify({
                'success': False, 
                'error': 'No puedes eliminar tu propio usuario'
            }), 400
        
        # Verificar que el usuario exista
        user = Usuario.get_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'Usuario no encontrado'}), 404
        
        # Realizar la eliminación lógica
        result = Usuario.delete(user_id)
        
        if result and result.get('affected_rows', 0) > 0:
            return jsonify({
                'success': True, 
                'message': 'Usuario eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'No se pudo eliminar el usuario'
            }), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
