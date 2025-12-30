import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

class Config:
    # Configuración de la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'ferreteria_secret_key_2024')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Configuración de la base de datos
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'ferreteria_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': os.getenv('DB_PORT', '3307')
    }
    
    # Configuración de la API
    API_PREFIX = '/api/v1'
