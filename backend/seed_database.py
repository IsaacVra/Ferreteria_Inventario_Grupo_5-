import os
import mysql.connector
from dotenv import load_dotenv
from utils.security import hash_password

# Cargar variables de entorno
load_dotenv()

def get_db_connection():
    """Establece conexión a la base de datos"""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'ferreteria_db')
    )

def execute_query(query, params=None, fetch=False):
    """Ejecuta una consulta SQL y devuelve los resultados si es necesario"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
            
        return result
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def insert_tipos_usuario():
    """Inserta los tipos de usuario en la base de datos"""
    tipos_usuario = [
        ('Administrador', 'Acceso total al sistema'),
        ('Gerente', 'Gestión de operaciones y personal'),
        ('Jefe de Bodega', 'Gestión de inventario'),
        ('Comprador', 'Gestión de compras a proveedores'),
        ('Vendedor', 'Registro de ventas')
    ]
    
    for tipo in tipos_usuario:
        # Verificar si el tipo ya existe
        check_query = "SELECT id_tipo_usuario FROM TIPO_USUARIO WHERE nombre_tipo = %s"
        existing = execute_query(check_query, (tipo[0],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO TIPO_USUARIO (nombre_tipo, descripcion)
            VALUES (%s, %s)
            """
            execute_query(query, tipo)
    
    print("Tipos de usuario insertados correctamente")

def insert_usuarios():
    """Inserta usuarios de ejemplo con contraseñas hasheadas"""
    usuarios = [
        {
            'cedula': '1712345678',
            'nombres': 'Kenny',
            'apellidos': 'Chung Velastegui',
            'usuario_login': 'kenny.admin',
            'password': 'admin123',  # Contraseña en texto plano
            'email': 'kenny@ferreteria.com',
            'telefono': '09987654321',
            'id_tipo_usuario': 1  # Administrador
        },
        {
            'cedula': '1723456789',
            'nombres': 'Isaac',
            'apellidos': 'Kalef Vera Villalba',
            'usuario_login': 'isaac.manager',
            'password': 'gerente123',
            'email': 'isaac@ferreteria.com',
            'telefono': '09987654322',
            'id_tipo_usuario': 2  # Gerente
        },
        {
            'cedula': '1734567890',
            'nombres': 'Valeria',
            'apellidos': 'Mero Zambrano',
            'usuario_login': 'valeria.jefe',
            'password': 'bodega123',
            'email': 'valeria@ferreteria.com',
            'telefono': '09987654323',
            'id_tipo_usuario': 3  # Jefe de Bodega
        },
        {
            'cedula': '1745678901',
            'nombres': 'Ana',
            'apellidos': 'Vendedor',
            'usuario_login': 'ana.vendedor',
            'password': 'ventas123',
            'email': 'ana@ferreteria.com',
            'telefono': '09987654324',
            'id_tipo_usuario': 5  # Vendedor
        }
    ]
    
    for usuario in usuarios:
        # Verificar si el usuario ya existe
        check_query = "SELECT id_usuario FROM USUARIO WHERE usuario_login = %s"
        existing = execute_query(check_query, (usuario['usuario_login'],), fetch=True)
        
        if not existing:
            # Hashear la contraseña
            hashed_password = hash_password(usuario['password'])
            
            # Insertar el usuario
            query = """
            INSERT INTO USUARIO 
            (cedula, nombres, apellidos, usuario_login, clave_hash, email, telefono, id_tipo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                usuario['cedula'],
                usuario['nombres'],
                usuario['apellidos'],
                usuario['usuario_login'],
                hashed_password,
                usuario['email'],
                usuario['telefono'],
                usuario['id_tipo_usuario']
            )
            execute_query(query, params)
    
    print("Usuarios de ejemplo insertados correctamente")

def insert_categorias():
    """Inserta categorías de ejemplo"""
    categorias = [
        ('Herramientas Manuales', 'Herramientas manuales para construcción y reparación'),
        ('Herramientas Eléctricas', 'Herramientas eléctricas y accesorios'),
        ('Material Eléctrico', 'Cables, interruptores y accesorios eléctricos'),
        ('Pinturas y Acabados', 'Pinturas, brochas y materiales de acabado'),
        ('Fontanería', 'Tuberías, grifería y accesorios de fontanería'),
        ('Construcción', 'Cementos, bloques y materiales de construcción'),
        ('Fijaciones', 'Tornillos, clavos y elementos de fijación'),
        ('Seguridad', 'Equipos de protección personal y seguridad')
    ]
    
    for categoria in categorias:
        # Verificar si la categoría ya existe
        check_query = "SELECT id_categoria FROM CATEGORIA WHERE nombre_categoria = %s"
        existing = execute_query(check_query, (categoria[0],), fetch=True)
        
        if not existing:
            query = """
            INSERT INTO CATEGORIA (nombre_categoria, descripcion)
            VALUES (%s, %s)
            """
            execute_query(query, categoria)
    
    print("Categorías insertadas correctamente")

def main():
    print("Iniciando la carga de datos de ejemplo...")
    
    try:
        # Insertar datos en orden de dependencia
        insert_tipos_usuario()
        insert_usuarios()
        insert_categorias()
        
        print("\n¡Datos de ejemplo cargados exitosamente!")
        
    except Exception as e:
        print(f"\nError al cargar los datos: {e}")
        print("Asegúrate de que la base de datos esté creada y las credenciales sean correctas.")
        print("Puedes configurar las credenciales en el archivo .env")

if __name__ == "__main__":
    main()
