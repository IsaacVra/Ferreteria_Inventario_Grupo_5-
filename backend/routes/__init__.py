# Este archivo permite que Python trate el directorio como un paquete
# Aquí podemos inicializar el Blueprint principal si es necesario

from .auth import auth_bp
from .users import users_bp
from .products import products_bp
from .categories import categories_bp
from .providers import providers_bp
from .dashboard import dashboard_bp
from .sales import sales_bp
from .customers import customers_bp

__all__ = [
    'auth_bp',
    'users_bp',
    'products_bp',
    'categories_bp',
    'providers_bp',
    'dashboard_bp',
    'sales_bp',
    'customers_bp'
]
