from functools import wraps
from flask import jsonify, session

def login_required(f):
    """
    Decorador para verificar si el usuario está autenticado.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    """
    Decorador para verificar si el usuario tiene los roles necesarios.
    
    Args:
        *roles: Lista de roles permitidos
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session:
                return jsonify({'error': 'No autorizado'}), 401
            
            user_role = session.get('role')
            if user_role not in roles:
                return jsonify({'error': 'Permiso denegado'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
