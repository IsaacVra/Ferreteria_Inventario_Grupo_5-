# Sistema de Inventario Ferretería - Instrucciones de Instalación

## Pasos para poner en marcha el sistema completo

### 1. Configurar la Base de Datos MySQL

1.1. Instalar MySQL si no lo tienes:
   - Descargar desde: https://dev.mysql.com/downloads/mysql/
   - O usar XAMPP/WAMP que incluye MySQL

1.2. Crear la base de datos:
```sql
CREATE DATABASE ferreteria_db;
```

1.3. Ejecutar el script de estructura:
   - Abrir MySQL Workbench o phpMyAdmin
   - Importar el archivo: `Ferreteria_Base.sql`

1.4. Ejecutar el script de datos de ejemplo:
   - Importar el archivo: `backend/datos_ejemplo.sql`

### 2. Configurar el Backend Python

2.1. Abrir terminal o cmd en la carpeta `backend`

2.2. Crear entorno virtual:
```bash
python -m venv venv
```

2.3. Activar entorno virtual:
```bash
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2.4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2.5. Configurar conexión a MySQL (si es necesario):
   - Editar `backend/app.py`
   - Modificar las variables en `DB_CONFIG`:
```python
DB_CONFIG = {
    'host': 'localhost',        # o tu servidor MySQL
    'database': 'ferreteria_db',
    'user': 'root',             # tu usuario MySQL
    'password': '',             # tu contraseña MySQL
    'port': '3306'
}
```

2.6. Iniciar el servidor backend:
```bash
python app.py
```
El servidor se iniciará en: http://localhost:5000

### 3. Configurar el Frontend

3.1. Abrir el archivo `ings .html` en un navegador web
   - Puedes hacer doble clic en el archivo
   - O usar un servidor web como Apache/Nginx

3.2. El frontend automáticamente se conectará al backend en http://localhost:5000

### 4. Probar el Sistema

4.1. Usuarios de prueba disponibles:
   - **kenny.admin** / **admin123** (Administrador)
   - **isaac.manager** / **gerente123** (Gerente)
   - **valeria.jefe** / **bodega123** (Jefe de Bodega)
   - **ana.vendedor** / **ventas123** (Vendedor)

4.2. Funcionalidades principales:
   - Login y autenticación
   - Dashboard con estadísticas
   - Gestión de productos
   - Gestión de ventas
   - Gestión de usuarios
   - Reportes

## Estructura Final del Proyecto

```
Ferreteria_Inventario_Grupo_5-/
├── Ferreteria_Base.sql          # Estructura de la base de datos
├── backend/
│   ├── app.py                   # Servidor Flask
│   ├── requirements.txt         # Dependencias Python
│   ├── datos_ejemplo.sql       # Datos de ejemplo
│   └── README.md               # Documentación backend
├── frontend/
│   └── app.js                  # JavaScript del frontend
├── "ings .html"                # Página principal del sistema
└── README_INSTALACION.md       # Este archivo
```

## Solución de Problemas Comunes

### Error de conexión a MySQL
- Verificar que MySQL esté corriendo
- Confirmar usuario y contraseña
- Verificar que la base de datos `ferreteria_db` exista

### Error de CORS en el navegador
- Asegurarse que el backend esté corriendo en http://localhost:5000
- Verificar que no haya firewalls bloqueando el puerto 5000

### El frontend no carga datos
- Abrir la consola del navegador (F12) para ver errores
- Verificar que el backend esté iniciado
- Confirmar que la URL del API sea correcta

## Soporte

Si tienes problemas, revisa:
1. La consola del navegador para errores de JavaScript
2. La terminal del backend para errores de Python
3. Los logs de MySQL para errores de base de datos

## Siguiente Paso

Una vez que el sistema esté funcionando, puedes:
- Agregar más funcionalidades
- Personalizar el diseño
- Agregar más reportes
- Implementar módulos adicionales
