import os
from flask import Flask, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar configuraciones
from config import Config

# Inicializar la aplicación Flask
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

# Configurar CORS
CORS(app, supports_credentials=True)

# Importar blueprints de rutas
from routes.auth import auth_bp
from routes.users import users_bp
from routes.products import products_bp
from routes.categories import categories_bp
from routes.providers import providers_bp
from routes.dashboard import dashboard_bp
from routes.sales import sales_bp
from routes.customers import customers_bp

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(providers_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(customers_bp)

# Ruta de verificación de salud
@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API."""
    return jsonify({
        'status': 'ok',
        'message': 'API de Ferretería en funcionamiento',
        'environment': 'development' if Config.DEBUG else 'production'
    })

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
