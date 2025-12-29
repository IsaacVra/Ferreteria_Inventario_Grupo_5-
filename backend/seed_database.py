import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from utils.security import hash_password
from database.database import db
from decimal import Decimal

# Cargar variables de entorno
load_dotenv()



def execute_query(query, params=None, fetch=False):
    """
    Ejecuta una consulta SQL utilizando la conexión de base de datos existente.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, optional): Parámetros para la consulta
        fetch (bool): Si es True, devuelve los resultados de la consulta
        
    Returns:
        list/dict: Resultados si fetch=True, de lo contrario el ID de la última fila insertada
    """
    if fetch:
        return db.execute_query(query, params, fetch=True)
    else:
        result = db.execute_query(query, params, fetch=False, commit=True)
        if query.strip().upper().startswith('INSERT'):
            return result['lastrowid']
        return result['affected_rows'] if result else 0

def insert_tipos_usuario():
    """Inserta los tipos de usuario básicos"""
    tipos = [
        ('Administrador', 'Acceso completo al sistema'),
        ('Gerente', 'Gestiona operaciones y personal'),
        ('Jefe de Bodega', 'Control de inventario y compras'),
        ('Vendedor', 'Atención al cliente y ventas'),
        ('Contador', 'Gestión financiera y reportes')
    ]
    
    for tipo in tipos:
        check_query = "SELECT id_tipo_usuario FROM TIPO_USUARIO WHERE nombre_tipo = %s"
        existing = execute_query(check_query, (tipo[0],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO TIPO_USUARIO (nombre_tipo, descripcion, estado)
            VALUES (%s, %s, 'ACTIVO')
            """
            execute_query(query, tipo)
    
    print("Tipos de usuario insertados correctamente")

# In seed_database.py, update the insert_usuarios function:
def insert_usuarios():
    """Inserta usuarios de ejemplo con contraseñas hasheadas"""
    usuarios = [
        ('kenny.admin', 'Kenny', 'Admin', 'admin@ferreteria.com', '0999999999', 'admin123', 1),
        ('isaac.manager', 'Isaac', 'Manager', 'gerente@ferreteria.com', '0987654321', 'gerente123', 2),
        ('bodega1', 'Carlos', 'Mendoza', 'bodega@ferreteria.com', '0976543210', 'bodega123', 3),
        ('vendedor1', 'Ana', 'Pérez', 'vendedor@ferreteria.com', '0965432109', 'vendedor123', 4),
        ('contador1', 'Luis', 'Martínez', 'contador@ferreteria.com', '0954321098', 'contador123', 5)
    ]
    
    for user in usuarios:
        check_query = "SELECT id_usuario FROM USUARIO WHERE usuario_login = %s"
        existing = execute_query(check_query, (user[0],), fetch=True)
        
        if not existing:
            # Get the plain text password
            plain_password = user[5]
            # Hash the password
            hashed_password = hash_password(plain_password)
            
            query = """
            INSERT INTO USUARIO (
                cedula, nombres, apellidos, email, telefono, 
                usuario_login, clave_hash, estado, id_tipo_usuario
            ) VALUES (CONCAT('17', LPAD(%s, 8, '0')), %s, %s, %s, %s, %s, %s, 'ACTIVO', %s)
            """
            execute_query(query, (
                str(random.randint(10000000, 99999999)),  # Generate a random ID
                user[1],  # First name
                user[2],  # Last name
                user[3],  # Email
                user[4],  # Phone
                user[0],  # Username
                hashed_password,  # Hashed password
                user[6]   # User type ID
            ))
    
    print("Test users inserted successfully")
    return execute_query("SELECT id_usuario, usuario_login FROM USUARIO", fetch=True)
        
def insert_categorias():
    """Inserta categorías de productos de ejemplo"""
    categorias = [
        ('Herramientas Manuales', 'Herramientas de uso manual como martillos, destornilladores, etc.'),
        ('Herramientas Eléctricas', 'Herramientas que funcionan con electricidad'),
        ('Materiales de Construcción', 'Materiales básicos para construcción'),
        ('Pinturas', 'Pinturas y accesorios para pintura'),
        ('Fontanería', 'Artículos para instalaciones de agua'),
        ('Eléctricos', 'Material eléctrico y cables'),
        ('Ferretería General', 'Artículos varios de ferretería'),
        ('Seguridad Industrial', 'Equipos de protección personal')
    ]
    
    for cat in categorias:
        check_query = "SELECT id_categoria FROM CATEGORIA WHERE nombre_categoria = %s"
        existing = execute_query(check_query, (cat[0],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO CATEGORIA (nombre_categoria, descripcion, estado)
            VALUES (%s, %s, 'ACTIVO')
            """
            execute_query(query, cat)
    
    print("Categorías insertadas correctamente")
    return execute_query("SELECT id_categoria, nombre_categoria FROM CATEGORIA", fetch=True)

def insert_proveedores():
    """Inserta proveedores de ejemplo"""
    proveedores = [
        ('Ferretería Industrial S.A.', '1798765434001', '022345678', 'ventas@ferreteriaindustrial.com', 'Av. Principal 123 y Calle 10'),
        ('Distribuidora de Materiales S.A.', '1798765434002', '022345679', 'contacto@dismasa.com', 'Calle F 456 y Av. Segunda'),
        ('Herramientas Profesionales Cía. Ltda.', '1798765434003', '022345680', 'info@herramientaspro.com', 'Calle del Comercio 789'),
        ('Eléctricos y Más', '1798765434004', '022345681', 'ventas@electricosymas.com', 'Av. 10 de Agosto N45-67'),
        ('Pinturas y Más', '1798765434005', '022345682', 'info@pinturasy.com', 'Calle de los Pinos 234')
    ]
    
    for prov in proveedores:
        check_query = "SELECT id_proveedor FROM PROVEEDOR WHERE ruc = %s"
        existing = execute_query(check_query, (prov[1],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO PROVEEDOR (nombre_comercial, ruc, telefono, email, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, 'ACTIVO')
            """
            execute_query(query, prov)
    
    print("Proveedores insertados correctamente")
    return execute_query("SELECT id_proveedor, nombre_comercial FROM PROVEEDOR", fetch=True)

def insert_clientes():
    """Inserta clientes de ejemplo"""
    clientes = [
        ('Juan', 'Pérez García', '1712345678', '0998765432', 'juan.perez@email.com', 'Av. Amazonas 1234'),
        ('María', 'González López', '1723456789', '0998765433', 'maria.gonzalez@email.com', 'Calle Roca 456'),
        ('Carlos', 'Martínez Vásquez', '1734567890', '0998765434', 'carlos.martinez@email.com', 'Av. 6 de Diciembre 789'),
        ('Ana', 'Rodríguez Pazmiño', '1745678901', '0998765435', 'ana.rodriguez@email.com', 'Av. Naciones Unidas 1001'),
        ('Luis', 'Torres Zambrano', '1756789012', '0998765436', 'luis.torres@email.com', 'Av. de los Shyris 234')
    ]
    
    for cli in clientes:
        check_query = "SELECT id_cliente FROM CLIENTE WHERE identificacion = %s"
        existing = execute_query(check_query, (cli[2],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO CLIENTE (nombres, apellidos, identificacion, telefono, email, direccion, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVO')
            """
            execute_query(query, cli)
    
    print("Clientes insertados correctamente")
    return execute_query("SELECT id_cliente, CONCAT(nombres, ' ', apellidos) as nombre_completo FROM CLIENTE", fetch=True)

def insert_productos(categorias, proveedores):
    """Inserta productos de ejemplo"""
    productos = [
        # ID, Código, Nombre, Descripción, Precio compra, Precio venta, Stock, Mínimo, Categoría, Proveedor
        ('MARTI-001', 'Martillo de Acero 16oz', 'Martillo de acero con mango de fibra de vidrio', 8.50, 12.99, 50, 10, 1, 1),
        ('TALA-001', 'Taladro Percutor 1/2"', 'Taladro percutor inalámbrico 20V', 89.99, 129.99, 15, 5, 2, 2),
        ('TORQ-001', 'Juego de Destornilladores', 'Juego de 6 destornilladores de precisión', 12.99, 19.99, 30, 8, 1, 3),
        ('PINT-001', 'Pintura Blanca Mate 1L', 'Pintura látex mate para interiores', 7.99, 12.50, 40, 10, 4, 5),
        ('CABL-001', 'Cable Eléctrico 2.5mm 100m', 'Cable THHN 2.5mm negro 100 metros', 45.99, 69.99, 25, 5, 6, 4),
        ('HERR-001', 'Alicate de Corte Diagonal 6"', 'Alicate de corte diagonal profesional', 5.99, 9.99, 35, 10, 1, 1),
        ('SEGU-001', 'Guantes de Seguridad Talla L', 'Guantes de seguridad anticorte', 4.50, 7.99, 60, 15, 8, 2),
        ('FONT-001', 'Llave de Paso 1/2"', 'Llave de paso de bronce para agua', 3.99, 6.99, 45, 10, 5, 3)
    ]
    
    for prod in productos:
        check_query = "SELECT id_producto FROM PRODUCTO WHERE codigo_producto = %s"
        existing = execute_query(check_query, (prod[0],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO PRODUCTO (
                codigo_producto, nombre_producto, descripcion, precio_compra_ref, 
                precio_venta, stock_actual, stock_minimo, id_categoria, id_proveedor, estado
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO')
            """
            execute_query(query, prod)
    
    print("Productos insertados correctamente")
    return execute_query("""
        SELECT p.id_producto, p.precio_venta, p.stock_actual, pr.nombre_comercial as proveedor 
        FROM PRODUCTO p 
        JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
    """, fetch=True)

def insert_compras(proveedores, productos, usuarios):
    """Inserta compras de ejemplo"""
    compras = []
    for i in range(5):  # Crear 5 compras de ejemplo
        proveedor = random.choice(proveedores)
        usuario = random.choice([u for u in usuarios if u['id_tipo_usuario'] in [1, 2, 3, 4]])  # Solo usuarios con permisos de compra
        
        # Crear la compra
        query = """
        INSERT INTO COMPRA (id_proveedor, id_usuario, total, estado, numero_factura)
        VALUES (%s, %s, %s, 'RECIBIDA', CONCAT('FAC-', LPAD(%s, 6, '0')))
        """
        total = 0
        compra_id = execute_query(query, (
            proveedor['id_proveedor'], 
            usuario['id_usuario'], 
            total, 
            i+1
        ))
        
        # Agregar 2-4 productos a cada compra
        num_productos = random.randint(2, 4)
        productos_compra = random.sample(productos, num_productos)
        
        for prod in productos_compra:
            cantidad = random.randint(5, 20)
            precio = Decimal(str(prod['precio_venta'])) * Decimal('0.8')  # 20% de descuento sobre el precio de venta
            subtotal = cantidad * precio
            
            query = """
            INSERT INTO DETALLE_COMPRA (id_compra, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            """
            execute_query(query, (compra_id, prod['id_producto'], cantidad, precio))
            
            # Actualizar stock del producto
            query = """
            UPDATE PRODUCTO 
            SET stock_actual = stock_actual + %s
            WHERE id_producto = %s
            """
            execute_query(query, (cantidad, prod['id_producto']))
            
            # Registrar movimiento de inventario
            query = """
            INSERT INTO MOVIMIENTO_INVENTARIO (
                tipo_movimiento, cantidad, motivo,
                stock_anterior, stock_nuevo, referencia,
                id_producto, id_usuario
            ) VALUES (
                'ENTRADA', %s, 'COMPRA', 
                %s, %s, CONCAT('COMP-', %s),
                %s, %s
            )
            """
            execute_query(query, (
                cantidad,
                prod['stock_actual'],
                prod['stock_actual'] + cantidad,
                compra_id,
                prod['id_producto'],
                usuario['id_usuario']
            ))
            
            total += subtotal
        
        # Actualizar el total de la compra
        query = "UPDATE COMPRA SET total = %s WHERE id_compra = %s"
        execute_query(query, (total, compra_id))
        
        compras.append({'id_compra': compra_id, 'total': total})
    
    print("Compras insertadas correctamente")
    return compras

def insert_ventas(clientes, productos, usuarios):
    """Inserta ventas de ejemplo"""
    ventas = []
    for i in range(10):  # Crear 10 ventas de ejemplo
        cliente = random.choice(clientes)
        usuario = random.choice([u for u in usuarios if u['id_tipo_usuario'] in [1, 2, 4]])  # Solo usuarios con permisos de venta
        fecha = datetime.now() - timedelta(days=random.randint(1, 30))
        
        # Crear la venta
        query = """
        INSERT INTO VENTA (
            id_cliente, id_usuario, total, estado, 
            tipo_comprobante, numero_comprobante, fecha_hora
        ) VALUES (%s, %s, %s, 'COMPLETADA', 'FACTURA', 
                 CONCAT('001-001-', LPAD(%s, 9, '0')), %s)
        """
        total = 0
        venta_id = execute_query(query, (
            cliente['id_cliente'], 
            usuario['id_usuario'], 
            total, 
            i+1,
            fecha.strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        # Agregar 1-3 productos a cada venta
        num_productos = random.randint(1, 3)
        productos_venta = random.sample(productos, num_productos)
        
        for prod in productos_venta:
            stock_query = "SELECT stock_actual FROM PRODUCTO WHERE id_producto = %s"
            stock = execute_query(stock_query, (prod['id_producto'],), fetch=True)[0]['stock_actual']
            
            if stock > 0:
                cantidad = random.randint(1, min(5, stock))  # No vender más del stock disponible
                precio = prod['precio_venta']
                subtotal = cantidad * precio
                
                query = """
                INSERT INTO DETALLE_VENTA (id_venta, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (venta_id, prod['id_producto'], cantidad, precio))
                
                # Actualizar stock del producto
                query = """
                UPDATE PRODUCTO 
                SET stock_actual = stock_actual - %s
                WHERE id_producto = %s
                """
                execute_query(query, (cantidad, prod['id_producto']))
                
                # Registrar movimiento de inventario
                query = """
                INSERT INTO MOVIMIENTO_INVENTARIO (
                    tipo_movimiento, cantidad, motivo,
                    stock_anterior, stock_nuevo, referencia,
                    id_producto, id_usuario
                ) VALUES (
                    'SALIDA', %s, 'VENTA', 
                    %s, %s, CONCAT('VENT-', %s),
                    %s, %s
                )
                """
                execute_query(query, (
                    cantidad,
                    stock,
                    stock - cantidad,
                    venta_id,
                    prod['id_producto'],
                    usuario['id_usuario']
                ))
                
                total += subtotal
        
        # Actualizar el total de la venta
        query = "UPDATE VENTA SET total = %s WHERE id_venta = %s"
        execute_query(query, (total, venta_id))
        
        ventas.append({'id_venta': venta_id, 'total': total})
    
    print("Ventas insertadas correctamente")
    return ventas

def insert_movimientos_inventario(usuarios, productos):
    """Inserta movimientos de inventario de ejemplo"""
    for _ in range(20):  # Crear 20 movimientos de inventario
        producto = random.choice(productos)
        usuario = random.choice(usuarios)
        tipo = random.choice(['ENTRADA', 'SALIDA', 'AJUSTE'])
        cantidad = random.randint(1, 10)
        
        # Obtener stock actual
        query = "SELECT stock_actual FROM PRODUCTO WHERE id_producto = %s"
        stock_actual = execute_query(query, (producto['id_producto'],), fetch=True)[0]['stock_actual']
        
        if tipo == 'ENTRADA':
            nuevo_stock = stock_actual + cantidad
        elif tipo == 'SALIDA' and stock_actual > cantidad:
            nuevo_stock = stock_actual - cantidad
        else:  # AJUSTE o SALIDA sin stock suficiente
            nuevo_stock = random.randint(1, 50)
            tipo = 'AJUSTE'
        
        motivo = f"{tipo.capitalize()} de inventario - {random.choice(['Ajuste de stock', 'Conteo físico', 'Devolución', 'Merma'])}"
        
        query = """
        INSERT INTO MOVIMIENTO_INVENTARIO (
            tipo_movimiento, cantidad, motivo,
            stock_anterior, stock_nuevo, referencia,
            id_producto, id_usuario
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (
            tipo,
            abs(nuevo_stock - stock_actual),
            motivo,
            stock_actual,
            nuevo_stock,
            f"MOV-{random.randint(1000, 9999)}",
            producto['id_producto'],
            usuario['id_usuario']
        ))
        
        # Actualizar stock del producto
        query = "UPDATE PRODUCTO SET stock_actual = %s WHERE id_producto = %s"
        execute_query(query, (nuevo_stock, producto['id_producto']))
    
    print("Movimientos de inventario insertados correctamente")

def insert_historial_acciones(usuarios):
    """Inserta registros de ejemplo en el historial de acciones"""
    entidades = ['USUARIO', 'PRODUCTO', 'CLIENTE', 'PROVEEDOR', 'VENTA', 'COMPRA']
    acciones = ['CREACION', 'ACTUALIZACION', 'ELIMINACION', 'INACTIVACION']
    
    for _ in range(30):  # Crear 30 registros de historial
        usuario = random.choice(usuarios)
        entidad = random.choice(entidades)
        accion = random.choice(acciones)
        id_registro = random.randint(1, 10)  # Asumiendo que hay al menos 10 registros en cada tabla
        
        descripcion = f"Se realizó {accion.lower()} en {entidad} con ID {id_registro}"
        
        query = """
        INSERT INTO HISTORIAL_ACCION (
            entidad_afectada, id_registro_afectado, tipo_accion,
            descripcion, ip_equipo, id_usuario
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (
            entidad,
            id_registro,
            accion,
            descripcion,
            f"192.168.1.{random.randint(1, 255)}",
            usuario['id_usuario']
        ))
    
    print("Historial de acciones insertado correctamente")


def limpiar_base_datos():
    """Elimina todos los datos de las tablas en el orden correcto"""
    print("Limpiando datos existentes...")
    tablas = [
        'HISTORIAL_ACCION', 'DETALLE_VENTA', 'DETALLE_COMPRA', 
        'MOVIMIENTO_INVENTARIO', 'VENTA', 'COMPRA', 
        'PRODUCTO', 'CLIENTE', 'PROVEEDOR', 
        'USUARIO', 'TIPO_USUARIO', 'CATEGORIA'
    ]
    
    try:
        # Desactivar temporalmente las restricciones de clave foránea
        execute_query("SET FOREIGN_KEY_CHECKS = 0")
        
        for tabla in tablas:
            execute_query(f"TRUNCATE TABLE {tabla}")
            print(f"  - Tabla {tabla} limpiada")
            
        # Reactivar las restricciones de clave foránea
        execute_query("SET FOREIGN_KEY_CHECKS = 1")
        print("Base de datos limpiada correctamente")
    except Exception as e:
        print(f"Error al limpiar la base de datos: {e}")
        raise

def main():
    print("Iniciando la carga de datos de ejemplo...")
    limpiar_base_datos()
    try:
        # Insertar datos en orden de dependencia
        insert_tipos_usuario()
        insert_usuarios()
        categorias = insert_categorias()
        
        # Insertar proveedores
        proveedores = insert_proveedores()
        
        # Insertar productos
        productos = insert_productos(categorias, proveedores)
        
        # Insertar clientes
        clientes = insert_clientes()
        
        # Obtener usuarios
        usuarios = execute_query("""
            SELECT u.id_usuario, u.id_tipo_usuario, t.nombre_tipo as tipo_usuario 
            FROM USUARIO u
            JOIN TIPO_USUARIO t ON u.id_tipo_usuario = t.id_tipo_usuario
        """, fetch=True)
        
        # Insertar compras
        compras = insert_compras(proveedores, productos, usuarios)
        
        # Insertar ventas
        ventas = insert_ventas(clientes, productos, usuarios)
        
        # Insertar movimientos de inventario adicionales
        insert_movimientos_inventario(usuarios, productos)
        
        # Insertar historial de acciones
        insert_historial_acciones(usuarios)
        
        print("\n¡Datos de ejemplo cargados exitosamente!")
        print(f"- {len(proveedores)} proveedores")
        print(f"- {len(productos)} productos")
        print(f"- {len(clientes)} clientes")
        print(f"- {len(compras)} compras")
        print(f"- {len(ventas)} ventas")
        print("- 20 movimientos de inventario adicionales")
        print("- 30 registros en el historial de acciones")
        
    except Exception as e:
        print(f"\nError al cargar los datos: {e}")
        print("Asegúrate de que la base de datos esté creada y las credenciales sean correctas.")
        print("Puedes configurar las credenciales en el archivo .env")


if __name__ == "__main__":
    main()