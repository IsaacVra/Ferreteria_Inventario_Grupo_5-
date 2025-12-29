from flask import Blueprint, request, jsonify
from database import db
from utils.decorators import login_required

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')

@customers_bp.route('', methods=['GET'])
@login_required
def get_customers():
    try:
        query = "SELECT * FROM CLIENTE WHERE estado = 'ACTIVO' ORDER BY nombres"
        result = db.execute_query(query)
        return jsonify({'customers': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('', methods=['POST'])
@login_required
def create_customer():
    try:
        data = request.get_json()
        
        required_fields = ['nombres', 'apellidos', 'identificacion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Verificar si el cliente ya existe
        check_query = "SELECT id_cliente FROM CLIENTE WHERE identificacion = %s"
        existing = db.execute_query(check_query, (data['identificacion'],))
        
        if existing:
            return jsonify({'error': 'El cliente ya existe'}), 400
        
        query = """
        INSERT INTO CLIENTE (nombres, apellidos, identificacion, telefono, email, direccion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data['nombres'],
            data['apellidos'],
            data['identificacion'],
            data.get('telefono', ''),
            data.get('email', ''),
            data.get('direccion', '')
        )
        
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({'success': True, 'message': 'Cliente creado correctamente'})
        else:
            return jsonify({'error': 'Error al crear cliente'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
