from flask import Blueprint, request, jsonify, session
from database import db
from utils.decorators import login_required

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@sales_bp.route('', methods=['GET'])
@login_required
def get_sales():
    try:
        query = """
        SELECT v.*, c.nombres as cliente_nombre, c.apellidos as cliente_apellido,
               u.nombres as vendedor_nombre, u.apellidos as vendedor_apellido
        FROM VENTA v
        JOIN CLIENTE c ON v.id_cliente = c.id_cliente
        JOIN USUARIO u ON v.id_usuario = u.id_usuario
        ORDER BY v.fecha_hora DESC
        LIMIT 50
        """
        
        result = db.execute_query(query)
        return jsonify({'sales': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('', methods=['POST'])
@login_required
def create_sale():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('id_cliente') or not data.get('detalles'):
            return jsonify({'error': 'Cliente y detalles son requeridos'}), 400
        
        detalles = data['detalles']
        if not isinstance(detalles, list) or len(detalles) == 0:
            return jsonify({'error': 'Los detalles deben ser una lista no vacía'}), 400
        
        # Calcular total y verificar stock
        total = 0
        for detalle in detalles:
            if not detalle.get('id_producto') or not detalle.get('cantidad') or not detalle.get('precio_unitario'):
                return jsonify({'error': 'Cada detalle debe tener id_producto, cantidad y precio_unitario'}), 400
            
            # Verificar stock disponible
            product_query = "SELECT stock_actual FROM PRODUCTO WHERE id_producto = %s AND estado = 'ACTIVO'"
            product_result = db.execute_query(product_query, (detalle['id_producto'],))
            
            if not product_result or product_result[0]['stock_actual'] < detalle['cantidad']:
                return jsonify({'error': f'Stock insuficiente para el producto {detalle["id_producto"]}'}), 400
            
            total += detalle['cantidad'] * detalle['precio_unitario']
        
        # Generar número de comprobante
        tipo_comprobante = data.get('tipo_comprobante', 'FACTURA')
        prefix = 'F' if tipo_comprobante == 'FACTURA' else 'B'
        
        # Obtener el último número de comprobante
        last_query = """
        SELECT MAX(numero_comprobante) as last_num 
        FROM VENTA 
        WHERE tipo_comprobante = %s AND numero_comprobante LIKE %s
        """
        last_result = db.execute_query(last_query, (tipo_comprobante, f'{prefix}%'))
        
        if last_result and last_result[0]['last_num']:
            last_num = int(last_result[0]['last_num'].split('-')[1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        numero_comprobante = f'{prefix}001-{new_num:03d}'
        
        # Crear la venta
        venta_query = """
        INSERT INTO VENTA (total, estado, tipo_comprobante, numero_comprobante, id_cliente, id_usuario)
        VALUES (%s, 'COMPLETADA', %s, %s, %s, %s)
        """
        
        venta_params = (total, tipo_comprobante, numero_comprobante, data['id_cliente'], session['user_id'])
        venta_result = db.execute_query(venta_query, venta_params)
        
        if not venta_result:
            return jsonify({'error': 'Error al crear la venta'}), 500
        
        id_venta = venta_result['lastrowid']
        
        # Crear detalles de venta y actualizar stock
        for detalle in detalles:
            # Insertar detalle
            detalle_query = """
            INSERT INTO DETALLE_VENTA (cantidad, precio_unitario, id_venta, id_producto)
            VALUES (%s, %s, %s, %s)
            """
            db.execute_query(detalle_query, (detalle['cantidad'], detalle['precio_unitario'], id_venta, detalle['id_producto']))
            
            # Actualizar stock
            update_query = """
            UPDATE PRODUCTO 
            SET stock_actual = stock_actual - %s 
            WHERE id_producto = %s
            """
            db.execute_query(update_query, (detalle['cantidad'], detalle['id_producto']))
            
            # Registrar movimiento de inventario
            movimiento_query = """
            INSERT INTO MOVIMIENTO_INVENTARIO 
            (tipo_movimiento, cantidad, motivo, stock_anterior, stock_nuevo, referencia, id_producto, id_usuario)
            VALUES ('SALIDA', %s, 'VENTA', 
                   (SELECT stock_actual + %s FROM PRODUCTO WHERE id_producto = %s),
                   (SELECT stock_actual FROM PRODUCTO WHERE id_producto = %s),
                   %s, %s, %s)
            """
            db.execute_query(movimiento_query, 
                           (detalle['cantidad'], detalle['cantidad'], detalle['id_producto'], 
                            detalle['id_producto'], numero_comprobante, detalle['id_producto'], session['user_id']))
        
        return jsonify({
            'success': True, 
            'message': 'Venta creada correctamente',
            'id_venta': id_venta,
            'numero_comprobante': numero_comprobante,
            'total': total
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
