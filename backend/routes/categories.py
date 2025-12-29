from flask import Blueprint, jsonify
from database import db
from utils.decorators import login_required

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET'])
@login_required
def get_categories():
    try:
        query = "SELECT * FROM CATEGORIA WHERE estado = 'ACTIVO' ORDER BY nombre_categoria"
        result = db.execute_query(query)
        return jsonify({'categories': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
