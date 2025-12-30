from flask import Blueprint, jsonify
from database import db
from utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    try:
        stats = {}
        
        # Total de productos
        result = db.execute_query("SELECT COUNT(*) as total FROM PRODUCTO WHERE estado = 'ACTIVO'")
        stats['total_products'] = result[0]['total'] if result else 0
        
        # Productos con bajo stock
        result = db.execute_query("""
            SELECT COUNT(*) as total FROM PRODUCTO 
            WHERE estado = 'ACTIVO' AND stock_actual <= stock_minimo
        """)
        stats['low_stock_products'] = result[0]['total'] if result else 0
        
        # Total de usuarios activos
        result = db.execute_query("SELECT COUNT(*) as total FROM USUARIO WHERE estado = 'ACTIVO'")
        stats['total_users'] = result[0]['total'] if result else 0
        
        # Ventas de hoy
        result = db.execute_query("""
            SELECT COUNT(*) as total, IFNULL(SUM(total), 0) as sum_total 
            FROM VENTA WHERE DATE(fecha_hora) = CURDATE()
        """)
        stats['today_sales_count'] = result[0]['total'] if result else 0
        stats['today_sales_amount'] = float(result[0]['sum_total']) if result and result[0]['sum_total'] else 0
        
        # Valor del inventario
        result = db.execute_query("""
            SELECT SUM(stock_actual * precio_compra_ref) as total_value 
            FROM PRODUCTO WHERE estado = 'ACTIVO'
        """)
        stats['inventory_value'] = float(result[0]['total_value']) if result and result[0]['total_value'] else 0
        
        return jsonify({'stats': stats})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/low-stock', methods=['GET'])
@login_required
def get_low_stock_products():
    try:
        query = """
        SELECT p.*, c.nombre_categoria
        FROM PRODUCTO p
        JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
        WHERE p.estado = 'ACTIVO' AND p.stock_actual <= p.stock_minimo
        ORDER BY p.stock_actual ASC
        LIMIT 10
        """
        
        result = db.execute_query(query)
        return jsonify({'products': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
