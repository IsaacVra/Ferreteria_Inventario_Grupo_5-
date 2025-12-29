from datetime import datetime
from database.database import db

class BaseModel:
    """Clase base para todos los modelos."""
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un registro por su ID."""
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id_{cls.TABLE_NAME} = %s"
        result = db.execute_query(query, (id,))
        return result[0] if result else None
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los registros de la tabla."""
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE estado = 'ACTIVO'"
        return db.execute_query(query)
    
    @classmethod
    def delete(cls, id):
        """Elimina lógicamente un registro."""
        query = f"""
            UPDATE {cls.TABLE_NAME} 
            SET estado = 'INACTIVO', fecha_actualizacion = %s 
            WHERE id_{cls.TABLE_NAME} = %s
        """
        return db.execute_query(
            query, 
            (datetime.now(), id),
            fetch=False,
            commit=True
        )

class Usuario(BaseModel):
    """Modelo para la tabla USUARIO."""
    TABLE_NAME = 'USUARIO'
    
    @classmethod
    def create(cls, data):
        """Crea un nuevo usuario."""
        query = """
            INSERT INTO USUARIO (
                nombres, apellidos, usuario_login, clave_hash, email,
                telefono, id_tipo_usuario, cedula, estado, fecha_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO', %s)
        """
        params = (
            data['nombres'],
            data['apellidos'],
            data['usuario_login'],
            data['clave_hash'],
            data['email'],
            data.get('telefono', ''),
            data['id_tipo_usuario'],
            data.get('cedula', ''),
            datetime.now()
        )
        return db.execute_query(query, params, fetch=False, commit=True)
    
    @classmethod
    def update(cls, user_id, data):
        """Actualiza un usuario existente."""
        query = """
            UPDATE USUARIO 
            SET nombres = %s,
                apellidos = %s,
                email = %s,
                telefono = %s,
                id_tipo_usuario = %s,
                cedula = %s,
                fecha_actualizacion = %s
            WHERE id_usuario = %s
        """
        params = (
            data['nombres'],
            data['apellidos'],
            data['email'],
            data.get('telefono', ''),
            data['id_tipo_usuario'],
            data.get('cedula', ''),
            datetime.now(),
            user_id
        )
        return db.execute_query(query, params, fetch=False, commit=True)

class Producto(BaseModel):
    """Modelo para la tabla PRODUCTO."""
    TABLE_NAME = 'PRODUCTO'
    
    @classmethod
    def create(cls, data):
        """
        Crea un nuevo producto.
        
        Args:
            data (dict): Diccionario con los datos del producto
                - codigo_producto (str): Código único del producto
                - nombre_producto (str): Nombre del producto
                - descripcion (str, optional): Descripción del producto
                - precio_compra_ref (float): Precio de compra de referencia
                - precio_venta (float): Precio de venta
                - stock_actual (int, optional): Stock actual (default: 0)
                - stock_minimo (int, optional): Stock mínimo permitido (default: 5)
                - unidad_medida (str, optional): Unidad de medida (default: 'UNIDAD')
                - id_categoria (int): ID de la categoría
                - id_proveedor (int): ID del proveedor
                
        Returns:
            dict: Resultado de la operación con el ID del producto creado
        """
        query = """
            INSERT INTO PRODUCTO (
                codigo_producto, nombre_producto, descripcion, precio_compra_ref,
                precio_venta, stock_actual, stock_minimo, unidad_medida,
                id_categoria, id_proveedor, estado, fecha_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'ACTIVO', %s)
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
            data['id_proveedor'],
            datetime.now()
        )
        return db.execute_query(query, params, fetch=False, commit=True)
    
    @classmethod
    def update(cls, product_id, data):
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto a actualizar
            data (dict): Diccionario con los campos a actualizar
                
        Returns:
            dict: Resultado de la operación
        """
        query = """
            UPDATE PRODUCTO 
            SET nombre_producto = %s,
                descripcion = %s,
                precio_compra_ref = %s,
                precio_venta = %s,
                stock_actual = %s,
                stock_minimo = %s,
                unidad_medida = %s,
                id_categoria = %s,
                id_proveedor = %s,
                fecha_actualizacion = %s
            WHERE id_producto = %s
        """
        # Obtener el producto actual para valores por defecto
        current = cls.get_by_id(product_id)
        if not current:
            return {'error': 'Producto no encontrado', 'status': 404}
            
        params = (
            data.get('nombre_producto', current['nombre_producto']),
            data.get('descripcion', current.get('descripcion', '')),
            data.get('precio_compra_ref', current['precio_compra_ref']),
            data.get('precio_venta', current['precio_venta']),
            data.get('stock_actual', current.get('stock_actual', 0)),
            data.get('stock_minimo', current.get('stock_minimo', 5)),
            data.get('unidad_medida', current.get('unidad_medida', 'UNIDAD')),
            data.get('id_categoria', current['id_categoria']),
            data.get('id_proveedor', current['id_proveedor']),
            datetime.now(),
            product_id
        )
        return db.execute_query(query, params, fetch=False, commit=True)
    
    @classmethod
    def get_by_codigo(cls, codigo):
        """Obtiene un producto por su código."""
        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE codigo_producto = %s AND estado = 'ACTIVO'"
        result = db.execute_query(query, (codigo,))
        return result[0] if result else None
    
    @classmethod
    def get_low_stock(cls):
        """Obtiene los productos con stock por debajo del mínimo."""
        query = """
            SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
            FROM PRODUCTO p
            JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
            JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
            WHERE p.stock_actual <= p.stock_minimo AND p.estado = 'ACTIVO'
            ORDER BY p.stock_actual ASC
        """
        return db.execute_query(query)

# Agrega aquí más modelos según sea necesario (Cliente, Venta, Categoría, etc.)
