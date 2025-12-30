from flask import Blueprint, request, jsonify
from database.models import Producto
from utils.decorators import login_required, roles_required

# Crear un Blueprint para las rutas de productos
products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route('', methods=['GET'])
@login_required
def get_products():
    """
    Obtiene todos los productos activos con información de categoría y proveedor.
    
    Query Parameters:
        - categoria (int, optional): Filtrar por ID de categoría
        - proveedor (int, optional): Filtrar por ID de proveedor
        - stock_min (int, optional): Filtrar productos con stock menor o igual a este valor
        - search (str, optional): Buscar por nombre o descripción
        
    Returns:
        JSON: Lista de productos con información relacionada
    """
    try:
        # Obtener parámetros de consulta
        categoria_id = request.args.get('categoria', type=int)
        proveedor_id = request.args.get('proveedor', type=int)
        stock_min = request.args.get('stock_min', type=int)
        search = request.args.get('search', '').strip()
        
        # Construir consulta base
        query = """
        SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
        FROM PRODUCTO p
        JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
        JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
        WHERE p.estado = 'ACTIVO'
        """
        
        params = []
        
        # Aplicar filtros
        if categoria_id:
            query += " AND p.id_categoria = %s"
            params.append(categoria_id)
            
        if proveedor_id:
            query += " AND p.id_proveedor = %s"
            params.append(proveedor_id)
            
        if stock_min is not None:
            query += " AND p.stock_actual <= %s"
            params.append(stock_min)
            
        if search:
            query += " AND (p.nombre_producto LIKE %s OR p.descripcion LIKE %s)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term])
        
        # Ordenar por nombre por defecto
        query += " ORDER BY p.nombre_producto"
        
        # Ejecutar consulta
        products = Producto.db.execute_query(query, tuple(params) if params else None)
        return jsonify({
            'success': True, 
            'data': products,
            'count': len(products)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products_bp.route('', methods=['POST'])
@login_required
@roles_required('ADMIN', 'INVENTARIO')
def create_product():
    """
    Crea un nuevo producto.
    
    Body (JSON):
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
        JSON: Producto creado con su ID
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = [
            'codigo_producto', 'nombre_producto', 'precio_compra_ref',
            'precio_venta', 'id_categoria', 'id_proveedor'
        ]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False, 
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Validar que el código no esté en uso
        existing = Producto.get_by_codigo(data['codigo_producto'])
        if existing:
            return jsonify({
                'success': False, 
                'error': 'Ya existe un producto con este código'
            }), 400
        
        # Validar precios
        if float(data['precio_venta']) <= 0 or float(data['precio_compra_ref']) <= 0:
            return jsonify({
                'success': False,
                'error': 'Los precios deben ser mayores a cero'
            }), 400
            
        if float(data['precio_venta']) < float(data['precio_compra_ref']):
            return jsonify({
                'success': False,
                'error': 'El precio de venta no puede ser menor al precio de compra'
            }), 400
        
        # Crear el producto
        product_data = {
            'codigo_producto': data['codigo_producto'].strip(),
            'nombre_producto': data['nombre_producto'].strip(),
            'descripcion': data.get('descripcion', '').strip(),
            'precio_compra_ref': float(data['precio_compra_ref']),
            'precio_venta': float(data['precio_venta']),
            'stock_actual': int(data.get('stock_actual', 0)),
            'stock_minimo': int(data.get('stock_minimo', 5)),
            'unidad_medida': data.get('unidad_medida', 'UNIDAD').strip(),
            'id_categoria': int(data['id_categoria']),
            'id_proveedor': int(data['id_proveedor'])
        }
        
        result = Producto.create(product_data)
        
        if result and 'lastrowid' in result:
            # Obtener el producto creado con información de relaciones
            query = """
            SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
            FROM PRODUCTO p
            JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
            JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
            WHERE p.id_producto = %s
            """
            new_product = Producto.db.execute_query(query, (result['lastrowid'],))
            
            return jsonify({
                'success': True, 
                'message': 'Producto creado correctamente',
                'data': new_product[0] if new_product else None
            }), 201
        else:
            return jsonify({
                'success': False, 
                'error': 'Error al crear el producto'
            }), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    """
    Obtiene un producto por su ID con información de categoría y proveedor.
    
    Args:
        product_id (int): ID del producto a buscar
        
    Returns:
        JSON: Datos del producto con información relacionada
    """
    try:
        query = """
        SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
        FROM PRODUCTO p
        JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
        JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
        WHERE p.id_producto = %s AND p.estado = 'ACTIVO'
        """
        
        product = Producto.db.execute_query(query, (product_id,))
        
        if product:
            return jsonify({
                'success': True, 
                'data': product[0]
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Producto no encontrado o inactivo'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al obtener el producto: {str(e)}'
        }), 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@login_required
@roles_required('ADMIN', 'INVENTARIO')
def update_product(product_id):
    """
    Actualiza un producto existente.
    
    Args:
        product_id (int): ID del producto a actualizar
        
    Body (JSON):
        Campos opcionales a actualizar:
        - codigo_producto (str): Nuevo código del producto
        - nombre_producto (str): Nuevo nombre
        - descripcion (str): Nueva descripción
        - precio_compra_ref (float): Nuevo precio de compra
        - precio_venta (float): Nuevo precio de venta
        - stock_actual (int): Nuevo stock actual
        - stock_minimo (int): Nuevo stock mínimo
        - unidad_medida (str): Nueva unidad de medida
        - id_categoria (int): Nueva categoría
        - id_proveedor (int): Nuevo proveedor
        
    Returns:
        JSON: Producto actualizado con información relacionada
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No se proporcionaron datos para actualizar'
            }), 400
        
        # Verificar si se está intentando actualizar el código
        if 'codigo_producto' in data:
            existing = Producto.get_by_codigo(data['codigo_producto'])
            if existing and existing['id_producto'] != product_id:
                return jsonify({
                    'success': False, 
                    'error': 'El código ya está en uso por otro producto'
                }), 400
        
        # Validar precios si se están actualizando
        if 'precio_venta' in data or 'precio_compra_ref' in data:
            precio_venta = float(data.get('precio_venta', 0))
            precio_compra = float(data.get('precio_compra_ref', 0))
            
            if precio_venta < precio_compra:
                return jsonify({
                    'success': False,
                    'error': 'El precio de venta no puede ser menor al precio de compra'
                }), 400
        
        # Preparar datos para actualización
        update_data = {}
        
        # Mapear campos del request a los nombres de columna de la base de datos
        field_mapping = {
            'codigo_producto': 'codigo_producto',
            'nombre_producto': 'nombre_producto',
            'descripcion': 'descripcion',
            'precio_compra_ref': 'precio_compra_ref',
            'precio_venta': 'precio_venta',
            'stock_actual': 'stock_actual',
            'stock_minimo': 'stock_minimo',
            'unidad_medida': 'unidad_medida',
            'id_categoria': 'id_categoria',
            'id_proveedor': 'id_proveedor'
        }
        
        # Solo incluir los campos que se están actualizando
        for field, db_field in field_mapping.items():
            if field in data:
                update_data[db_field] = data[field]
        
        # Realizar la actualización
        result = Producto.update(product_id, update_data)
        
        if isinstance(result, dict) and 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), result.get('status', 500)
        
        if result and result.get('affected_rows', 0) > 0:
            # Obtener el producto actualizado con información de relaciones
            query = """
            SELECT p.*, c.nombre_categoria, pr.nombre_comercial as proveedor
            FROM PRODUCTO p
            JOIN CATEGORIA c ON p.id_categoria = c.id_categoria
            JOIN PROVEEDOR pr ON p.id_proveedor = pr.id_proveedor
            WHERE p.id_producto = %s
            """
            updated_product = Producto.db.execute_query(query, (product_id,))
            
            return jsonify({
                'success': True, 
                'message': 'Producto actualizado correctamente',
                'data': updated_product[0] if updated_product else None
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'No se realizaron cambios en el producto'
            }), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@login_required
@roles_required('ADMIN', 'INVENTARIO')
def delete_product(product_id):
    """
    Elimina un producto de manera lógica (cambia su estado a INACTIVO).
    
    Args:
        product_id (int): ID del producto a eliminar
        
    Returns:
        JSON: Resultado de la operación
    """
    try:
        # Verificar si el producto existe y está activo
        product = Producto.get_by_id(product_id)
        if not product:
            return jsonify({
                'success': False, 
                'error': 'Producto no encontrado'
            }), 404
            
        # Verificar si el producto tiene stock
        if product.get('stock_actual', 0) > 0:
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar un producto con stock disponible'
            }), 400
        
        # Realizar la eliminación lógica
        result = Producto.delete(product_id)
        
        if result and result.get('affected_rows', 0) > 0:
            return jsonify({
                'success': True, 
                'message': 'Producto eliminado correctamente'
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'No se pudo eliminar el producto'
            }), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products_bp.route('/low-stock', methods=['GET'])
@login_required
def get_low_stock_products():
    """
    Obtiene los productos con stock por debajo del mínimo establecido.
    
    Query Parameters:
        - limit (int, optional): Limitar el número de resultados
        
    Returns:
        JSON: Lista de productos con stock bajo
    """
    try:
        limit = request.args.get('limit', type=int)
        
        # Usar el método del modelo para obtener productos con stock bajo
        products = Producto.get_low_stock()
        
        # Aplicar límite si se especificó
        if limit and limit > 0:
            products = products[:limit]
        
        return jsonify({
            'success': True, 
            'data': products,
            'count': len(products)
        })
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al obtener productos con bajo stock: {str(e)}'
        }), 500
