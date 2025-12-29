from flask import Blueprint, jsonify
from database import db
from utils.decorators import login_required

providers_bp = Blueprint('providers', __name__, url_prefix='/api/providers')

@providers_bp.route('', methods=['GET'])
@login_required
def get_providers():
    try:
        query = "SELECT * FROM PROVEEDOR WHERE estado = 'ACTIVO' ORDER BY nombre_comercial"
        result = db.execute_query(query)
        return jsonify({'providers': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
