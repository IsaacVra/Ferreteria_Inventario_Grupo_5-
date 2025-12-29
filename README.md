# Sistema de Gestión de Inventario - Ferretería

Sistema de gestión de inventario para ferretería desarrollado con Python (Flask) en el backend y JavaScript/HTML/CSS en el frontend.

## Requisitos Previos

- Python 3.10 o superior
- Node.js 16.x o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)
- npm (gestor de paquetes de Node.js)

## Configuración del Entorno de Desarrollo

### 1. Clonar el Repositorio

```bash
git clone https://github.com/IsaacVra/Ferreteria_Inventario_Grupo_5-.git
cd Ferreteria_Inventario_Grupo_5-
```

### 2. Configuración del Backend

1. **Crear y activar entorno virtual**
   ```bash
   # En Linux/MacOS
   python -m venv venv
   source venv/bin/activate

   # En Windows
   # python -m venv venv
   # .\venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**
   - Crear una base de datos MySQL llamada `ferreteria_db`
   - Importar el esquema inicial:
     ```bash
     mysql -u root -p ferreteria_db < Ferreteria_Base.sql
     ```
   - Configurar las variables de entorno creando un archivo `.env` en la carpeta `backend` con el siguiente contenido:
     ```
     DB_HOST=localhost
     DB_NAME=ferreteria_db
     DB_USER=tu_usuario
     DB_PASSWORD=tu_contraseña
     DB_PORT=3307
     SECRET_KEY=tu_clave_secreta_aqui
     DEBUG=True
     ```

4. **Poblar la base de datos con datos de ejemplo**
   ```bash
   python seed_database.py
   ```

5. **Iniciar el servidor de desarrollo**
   ```bash
   python app.py
   ```
   El servidor backend estará disponible en `http://localhost:5000`

### 3. Configuración del Frontend

1. **Instalar dependencias**
   ```bash
   cd ../frontend
   npm install
   ```

2. **Iniciar el servidor de desarrollo**
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:3000`

## Estructura del Proyecto

```
Ferreteria_Inventario_Grupo_5-/
├── backend/               # Código del servidor
│   ├── database/         # Configuración de la base de datos
│   ├── routes/           # Rutas de la API
│   ├── static/           # Archivos estáticos
│   ├── templates/        # Plantillas HTML
│   ├── utils/            # Utilidades
│   ├── .env              # Variables de entorno
│   ├── app.py            # Aplicación principal
│   ├── config.py         # Configuración
│   └── requirements.txt  # Dependencias de Python
└── frontend/             # Código del cliente
    ├── src/              # Código fuente
    ├── public/           # Archivos públicos
    └── package.json      # Dependencias de Node.js
```

## Usuarios de Prueba

El sistema incluye varios usuarios de prueba con diferentes roles:

- **Administrador**
  - Usuario: admin
  - Contraseña: admin123

- **Vendedor**
  - Usuario: vendedor1
  - Contraseña: vendedor123

- **Almacenero**
  - Usuario: almacen1
  - Contraseña: almacen123

## Despliegue en Producción

Para entornos de producción, se recomienda:

1. Configurar un servidor WSGI como Gunicorn
2. Configurar un servidor web como Nginx como proxy inverso
3. Configurar HTTPS con certificado SSL
4. Establecer `DEBUG=False` en las variables de entorno
5. Usar una base de datos en un servidor separado

## Solución de Problemas

### Error de conexión a la base de datos
- Verificar que el servicio de MySQL esté en ejecución
- Comprobar las credenciales en el archivo `.env`
- Asegurarse de que el puerto de MySQL sea el correcto (por defecto 3306 o 3307)

### Error al instalar dependencias
- Asegurarse de tener las versiones correctas de Python y Node.js
- Ejecutar `npm cache clean --force` y volver a instalar
- En Windows, instalar las herramientas de compilación de Python

## Contribución

1. Hacer fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un nuevo Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.