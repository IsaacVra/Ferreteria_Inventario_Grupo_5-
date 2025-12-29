from flask import Blueprint, request, session, jsonify
from database.models import Usuario
from database.database import db
from utils.security import check_password

# Crear un Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
        
        query = """
        SELECT u.*, tu.nombre_tipo as rol
        FROM USUARIO u
        JOIN TIPO_USUARIO tu ON u.id_tipo_usuario = tu.id_tipo_usuario
        WHERE u.usuario_login = %s AND u.estado = 'ACTIVO'
        """
        
        result = db.execute_query(query, (username,))
        
        if result and len(result) > 0 and check_password(password, result[0]['clave_hash']):
            user = result[0]
            session['user_id'] = user['id_usuario']
            session['username'] = user['usuario_login']
            session['role'] = user['rol']
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id_usuario'],
                    'username': user['usuario_login'],
                    'name': f"{user['nombres']} {user['apellidos']}",
                    'role': user['rol'],
                    'email': user['email']
                }
            })
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cierra la sesión del usuario actual."""
    session.clear()
    return jsonify({'success': True})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Obtiene la información del usuario actualmente autenticado."""
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    try:
        query = """
        SELECT u.id_usuario, u.usuario_login, u.nombres, u.apellidos, u.email, 
               u.estado, tu.nombre_tipo as rol
        FROM USUARIO u
        JOIN TIPO_USUARIO tu ON u.id_tipo_usuario = tu.id_tipo_usuario
        WHERE u.id_usuario = %s
        """
        
        result = db.execute_query(query, (session['user_id'],))
        
        if result:
            return jsonify({
                'success': True,
                'user': result[0]
            })
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
