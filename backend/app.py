from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import hashlib
import datetime
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'ferreteria_secret_key_2024'
CORS(app)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ferreteria_db',
    'user': 'root',
    'password': '',  # XAMPP por defecto no usa contraseña
    'port': '3307'  # XAMPP usa el puerto 3307
}

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos MySQL")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return {"affected_rows": cursor.rowcount, "lastrowid": cursor.lastrowid}
        except Error as e:
            print(f"Error en la consulta: {e}")
            return None

# Instancia global de la base de datos
db = Database()

# Decorador para requerir autenticación
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Rutas de autenticación
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
        
        hashed_password = hash_password(password)
        
        query = """
        SELECT u.*, tu.nombre_tipo as rol
        FROM USUARIO u
        JOIN TIPO_USUARIO tu ON u.id_tipo_usuario = tu.id_tipo_usuario
        WHERE u.usuario_login = %s AND u.clave_hash = %s AND u.estado = 'ACTIVO'
        """
        
        result = db.execute_query(query, (username, hashed_password))
        
        if result and len(result) > 0:
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

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# Rutas de usuarios
@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    try:
        query = """
        SELECT u.id_usuario, u.usuario_login, u.nombres, u.apellidos, u.email, 
               u.estado, tu.nombre_tipo as rol
        FROM USUARIO u
        JOIN TIPO_USUARIO tu ON u.id_tipo_usuario = tu.id_tipo_usuario
        WHERE u.estado = 'ACTIVO'
        ORDER BY u.nombres
        """
        
        result = db.execute_query(query)
        return jsonify({'users': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
@login_required
def create_user():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombres', 'apellidos', 'usuario_login', 'clave', 'email', 'id_tipo_usuario']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Verificar si el usuario ya existe
        check_query = "SELECT id_usuario FROM USUARIO WHERE usuario_login = %s OR email = %s"
        existing = db.execute_query(check_query, (data['usuario_login'], data['email']))
        
        if existing:
            return jsonify({'error': 'El usuario o email ya existe'}), 400
        
        # Insertar nuevo usuario
        query = """
        INSERT INTO USUARIO (nombres, apellidos, usuario_login, clave_hash, email, 
                           telefono, id_tipo_usuario, cedula)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data['nombres'],
            data['apellidos'],
            data['usuario_login'],
            hash_password(data['clave']),
            data['email'],
            data.get('telefono', ''),
            data['id_tipo_usuario'],
            data.get('cedula', '')
        )
        
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({'success': True, 'message': 'Usuario creado correctamente'})
        else:
            return jsonify({'error': 'Error al crear usuario'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas de productos
@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    try:
        query = """
        SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
        FROM PRODUCTO p
        JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
        JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
        WHERE p.estado = 'ACTIVO'
        ORDER BY p.nombre_producto
        """
        
        result = db.execute_query(query)
        return jsonify({'products': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
@login_required
def create_product():
    try:
        data = request.get_json()
        
        required_fields = ['codigo_producto', 'nombre_producto', 'precio_compra_ref', 
                          'precio_venta', 'id_categoria', 'id_proveedor']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        query = """
        INSERT INTO PRODUCTO (codigo_producto, nombre_producto, descripcion, 
                            precio_compra_ref, precio_venta, stock_actual, 
                            stock_minimo, unidad_medida, id_categoria, id_proveedor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            data['codigo_producto'],
            data['nombre_producto'],
            data.get('descripcion', ''),
            data['precio_compra_ref'],
            data['precio_venta'],
            data.get('stock_actual', 0),
            data.get('stock_minimo', 5),
            data.get('unidad_medida', 'UNIDAD'),
            data['id_categoria'],
            data['id_proveedor']
        )
        
        result = db.execute_query(query, params)
        
        if result:
            return jsonify({'success': True, 'message': 'Producto creado correctamente'})
        else:
            return jsonify({'error': 'Error al crear producto'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas de categorías
@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    try:
        query = "SELECT * FROM CATEGORIA WHERE estado = 'ACTIVO' ORDER BY nombre_categoria"
        result = db.execute_query(query)
        return jsonify({'categories': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas de proveedores
@app.route('/api/providers', methods=['GET'])
@login_required
def get_providers():
    try:
        query = "SELECT * FROM PROVEEDOR WHERE estado = 'ACTIVO' ORDER BY nombre_comercial"
        result = db.execute_query(query)
        return jsonify({'providers': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rutas de dashboard
@app.route('/api/dashboard/stats', methods=['GET'])
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

@app.route('/api/dashboard/low-stock', methods=['GET'])
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

# Rutas de ventas
@app.route('/api/sales', methods=['GET'])
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

@app.route('/api/sales', methods=['POST'])
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

# Rutas de clientes
@app.route('/api/customers', methods=['GET'])
@login_required
def get_customers():
    try:
        query = "SELECT * FROM CLIENTE WHERE estado = 'ACTIVO' ORDER BY nombres"
        result = db.execute_query(query)
        return jsonify({'customers': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
