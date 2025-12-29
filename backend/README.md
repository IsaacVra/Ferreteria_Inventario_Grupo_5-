# Sistema de Inventario Ferretería - Backend Python

## Requisitos
- Python 3.8+
- MySQL 5.7+
- Pip

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar base de datos:
   - Crear base de datos `ferreteria_db` en MySQL
   - Ejecutar el script `Ferreteria_Base.sql` para crear las tablas
   - Ejecutar `datos_ejemplo.sql` para insertar datos de ejemplo

4. Configurar conexión a la base de datos:
   - Editar el archivo `app.py`
   - Modificar las variables en `DB_CONFIG` según tu configuración de MySQL

## Ejecutar el servidor

```bash
python app.py
```

El servidor se iniciará en: http://localhost:5000

## API Endpoints

### Autenticación
- `POST /api/login` - Iniciar sesión
- `POST /api/logout` - Cerrar sesión

### Usuarios
- `GET /api/users` - Listar usuarios
- `POST /api/users` - Crear usuario

### Productos
- `GET /api/products` - Listar productos
- `POST /api/products` - Crear producto

### Ventas
- `GET /api/sales` - Listar ventas
- `POST /api/sales` - Crear venta

### Clientes
- `GET /api/customers` - Listar clientes
- `POST /api/customers` - Crear cliente

### Categorías
- `GET /api/categories` - Listar categorías

### Proveedores
- `GET /api/providers` - Listar proveedores

### Dashboard
- `GET /api/dashboard/stats` - Estadísticas del dashboard
- `GET /api/dashboard/low-stock` - Productos con bajo stock

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| kenny.admin | admin123 | Administrador |
| isaac.manager | gerente123 | Gerente |
| valeria.jefe | bodega123 | Jefe de Bodega |
| ana.vendedor | ventas123 | Vendedor |

## Estructura del proyecto

```
backend/
├── app.py              # Aplicación Flask principal
├── requirements.txt    # Dependencias Python
├── datos_ejemplo.sql   # Datos de ejemplo para la BD
└── README.md          # Este archivo
```
