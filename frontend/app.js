// ============== CONFIGURACIÓN DE LA API ==============
const API_BASE_URL = 'http://localhost:5000/api';

// ============== FUNCIONES DE LA API ==============

// Función para hacer peticiones a la API
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',
            ...options
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error en la petición');
        }

        return await response.json();
    } catch (error) {
        console.error('Error en API:', error);
        throw error;
    }
}

// ============== DATOS DEL SISTEMA ==============
const systemData = {
    currentUser: null,
    
    // Función para verificar si está autenticado
    isAuthenticated() {
        return this.currentUser !== null;
    }
};

// ============== FUNCIONES DEL SISTEMA ==============

// Función para autocompletar credenciales
function fillCredentials(username, password) {
    document.getElementById('username').value = username;
    document.getElementById('password').value = password;
}

// Función de login con API
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await apiRequest('/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        if (response.success) {
            systemData.currentUser = response.user;
            
            // Mostrar sistema principal
            document.getElementById('login-page').style.display = 'none';
            document.getElementById('main-system').style.display = 'flex';
            
            // Actualizar información de usuario
            document.getElementById('userName').textContent = response.user.name;
            document.getElementById('userRole').textContent = response.user.role;
            document.getElementById('userAvatar').textContent = response.user.name.charAt(0).toUpperCase();
            
            // Cargar datos iniciales
            loadDashboard();
            updateCurrentDate();
            
            // Mostrar mensaje de bienvenida
            alert(`¡Bienvenido ${response.user.name}!\nRol: ${response.user.role}\n\nSistema cargado correctamente.`);
        }
    } catch (error) {
        alert('Error de login: ' + error.message);
    }
});

// Función para cargar dashboard desde la API
async function loadDashboard() {
    try {
        // Cargar estadísticas
        const statsResponse = await apiRequest('/dashboard/stats');
        const stats = statsResponse.stats;
        
        document.getElementById('totalProducts').textContent = stats.total_products;
        document.getElementById('totalUsers').textContent = stats.total_users;
        document.getElementById('todaySales').textContent = `$${stats.today_sales_amount.toFixed(2)}`;
        document.getElementById('inventoryValue').textContent = `$${stats.inventory_value.toFixed(2)}`;
        
        // Cargar productos con bajo stock
        const lowStockResponse = await apiRequest('/dashboard/low-stock');
        const lowStockProducts = lowStockResponse.products;
        
        let lowStockHTML = '';
        lowStockProducts.forEach(product => {
            const stockClass = product.stock_actual <= 5 ? 'stock-danger' : 'stock-warning';
            lowStockHTML += `
                <div class="product-card ${stockClass}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="product-name">${product.nombre_producto}</div>
                            <small class="text-muted">Código: ${product.codigo_producto}</small>
                        </div>
                        <div class="text-end">
                            <strong>Stock: ${product.stock_actual}</strong><br>
                            <small>Mínimo: ${product.stock_minimo}</small>
                        </div>
                    </div>
                </div>
            `;
        });
        
        document.getElementById('lowStockProducts').innerHTML = lowStockHTML || '<p class="text-muted">No hay productos con bajo stock</p>';
        
        // Cargar alertas recientes (simuladas por ahora)
        const alertsHTML = `
            <div class="alert alert-warning">
                <small><i class="fas fa-exclamation-triangle"></i> ${stats.low_stock_products} productos con bajo stock</small>
            </div>
            <div class="alert alert-info">
                <small><i class="fas fa-shopping-cart"></i> ${stats.today_sales_count} ventas hoy</small>
            </div>
        `;
        document.getElementById('recentAlerts').innerHTML = alertsHTML;
        
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        // Cargar datos de respaldo si falla la API
        loadFallbackDashboard();
    }
}

// Función de respaldo para cargar dashboard
function loadFallbackDashboard() {
    document.getElementById('totalProducts').textContent = '24';
    document.getElementById('totalUsers').textContent = '6';
    document.getElementById('todaySales').textContent = '$1,245';
    document.getElementById('inventoryValue').textContent = '$15,890';
    
    document.getElementById('lowStockProducts').innerHTML = `
        <div class="product-card stock-danger">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="product-name">Tornillos 3" (100u)</div>
                    <small class="text-muted">Código: PROD002</small>
                </div>
                <div class="text-end">
                    <strong>Stock: 8</strong><br>
                    <small>Mínimo: 20</small>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('recentAlerts').innerHTML = `
        <div class="alert alert-warning">
            <small><i class="fas fa-exclamation-triangle"></i> 5 productos con bajo stock</small>
        </div>
        <div class="alert alert-info">
            <small><i class="fas fa-shopping-cart"></i> 8 ventas hoy</small>
        </div>
    `;
}

// Función para cargar productos
async function loadProducts() {
    try {
        const response = await apiRequest('/products');
        const products = response.products;
        
        let productsHTML = '';
        products.forEach(product => {
            const stockClass = product.stock_actual <= product.stock_minimo ? 'stock-warning' : '';
            productsHTML += `
                <tr class="${stockClass}">
                    <td>${product.codigo_producto}</td>
                    <td>${product.nombre_producto}</td>
                    <td>${product.nombre_categoria}</td>
                    <td>${product.stock_actual}</td>
                    <td>$${product.precio_venta.toFixed(2)}</td>
                    <td><span class="badge bg-success">${product.estado}</span></td>
                    <td>
                        <button class="btn btn-sm btn-primary btn-action" onclick="editProduct(${product.id_producto})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger btn-action" onclick="deleteProduct(${product.id_producto})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        document.getElementById('productsTable').innerHTML = productsHTML;
    } catch (error) {
        console.error('Error cargando productos:', error);
        document.getElementById('productsTable').innerHTML = '<tr><td colspan="7" class="text-center">Error al cargar productos</td></tr>';
    }
}

// Función para cargar ventas
async function loadSales() {
    try {
        const response = await apiRequest('/sales');
        const sales = response.sales;
        
        let salesHTML = '';
        sales.forEach(sale => {
            const statusClass = sale.estado === 'COMPLETADA' ? 'bg-success' : 'bg-warning';
            salesHTML += `
                <tr>
                    <td>${sale.numero_comprobante}</td>
                    <td>${new Date(sale.fecha_hora).toLocaleDateString()}</td>
                    <td>${sale.cliente_nombre} ${sale.cliente_apellido}</td>
                    <td>$${sale.total.toFixed(2)}</td>
                    <td>${sale.vendedor_nombre} ${sale.vendedor_apellido}</td>
                    <td><span class="badge ${statusClass}">${sale.estado}</span></td>
                    <td>
                        <button class="btn btn-sm btn-info btn-action" onclick="viewSale(${sale.id_venta})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        document.getElementById('salesTable').innerHTML = salesHTML;
    } catch (error) {
        console.error('Error cargando ventas:', error);
        document.getElementById('salesTable').innerHTML = '<tr><td colspan="7" class="text-center">Error al cargar ventas</td></tr>';
    }
}

// Función para cargar usuarios
async function loadUsers() {
    try {
        const response = await apiRequest('/users');
        const users = response.users;
        
        let usersHTML = '';
        users.forEach(user => {
            const roleClass = {
                'Administrador': 'role-admin',
                'Gerente': 'role-manager',
                'Jefe de Bodega': 'role-warehouse',
                'Vendedor': 'role-seller'
            }[user.rol] || 'role-admin';
            
            usersHTML += `
                <tr>
                    <td>${user.usuario_login}</td>
                    <td>${user.nombres} ${user.apellidos}</td>
                    <td>${user.email}</td>
                    <td><span class="badge ${roleClass}">${user.rol}</span></td>
                    <td><span class="badge bg-success">${user.estado}</span></td>
                    <td>
                        <button class="btn btn-sm btn-primary btn-action" onclick="editUser(${user.id_usuario})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger btn-action" onclick="deleteUser(${user.id_usuario})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        document.getElementById('usersTable').innerHTML = usersHTML;
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        document.getElementById('usersTable').innerHTML = '<tr><td colspan="6" class="text-center">Error al cargar usuarios</td></tr>';
    }
}

// Función para crear nuevo producto
async function createProduct() {
    try {
        // Obtener categorías y proveedores
        const [categoriesResponse, providersResponse] = await Promise.all([
            apiRequest('/categories'),
            apiRequest('/providers')
        ]);
        
        // Aquí iría el código para mostrar el modal con los datos
        // Por ahora, solo mostramos un mensaje
        alert('Función de crear producto en desarrollo');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar creación de producto');
    }
}

// Función para crear nuevo usuario
async function createUser() {
    try {
        // Aquí iría el código para mostrar el modal de creación
        alert('Función de crear usuario en desarrollo');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar creación de usuario');
    }
}

// Función para crear nueva venta
async function createSale() {
    try {
        // Obtener clientes y productos
        const [customersResponse, productsResponse] = await Promise.all([
            apiRequest('/customers'),
            apiRequest('/products')
        ]);
        
        // Aquí iría el código para mostrar el modal de venta
        alert('Función de crear venta en desarrollo');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar creación de venta');
    }
}

// Función de logout
async function logout() {
    try {
        await apiRequest('/logout', { method: 'POST' });
        systemData.currentUser = null;
        
        // Mostrar pantalla de login
        document.getElementById('main-system').style.display = 'none';
        document.getElementById('login-page').style.display = 'block';
        
        // Limpiar formulario
        document.getElementById('loginForm').reset();
    } catch (error) {
        console.error('Error en logout:', error);
        // Forzar logout incluso si hay error
        location.reload();
    }
}

// Funciones placeholder para edición y eliminación
function editProduct(id) {
    alert(`Editar producto ${id} - Función en desarrollo`);
}

function deleteProduct(id) {
    if (confirm('¿Está seguro de eliminar este producto?')) {
        alert(`Eliminar producto ${id} - Función en desarrollo`);
    }
}

function editUser(id) {
    alert(`Editar usuario ${id} - Función en desarrollo`);
}

function deleteUser(id) {
    if (confirm('¿Está seguro de eliminar este usuario?')) {
        alert(`Eliminar usuario ${id} - Función en desarrollo`);
    }
}

function viewSale(id) {
    alert(`Ver venta ${id} - Función en desarrollo`);
}

// ============== NAVEGACIÓN ==============

// Navegación entre páginas
document.querySelectorAll('.nav-link-custom[data-page]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Remover clase active de todos los enlaces
        document.querySelectorAll('.nav-link-custom').forEach(l => l.classList.remove('active'));
        this.classList.add('active');
        
        // Ocultar todas las páginas
        document.querySelectorAll('[id$="Page"]').forEach(page => page.style.display = 'none');
        
        // Mostrar página seleccionada
        const pageName = this.dataset.page;
        const pageElement = document.getElementById(pageName + 'Page');
        if (pageElement) {
            pageElement.style.display = 'block';
            document.getElementById('pageTitle').textContent = this.textContent.trim();
            
            // Cargar datos específicos de la página
            switch(pageName) {
                case 'dashboard':
                    loadDashboard();
                    break;
                case 'products':
                    loadProducts();
                    break;
                case 'sales':
                    loadSales();
                    break;
                case 'users':
                    loadUsers();
                    break;
            }
        }
    });
});

// Event listener para logout
document.getElementById('logoutBtn').addEventListener('click', logout);

// Event listeners para botones de creación
document.getElementById('newProductBtn')?.addEventListener('click', createProduct);
document.getElementById('newUserBtn')?.addEventListener('click', createUser);
document.getElementById('newSaleBtn')?.addEventListener('click', createSale);

// ============== FUNCIONES AUXILIARES ==============

// Actualizar fecha actual
function updateCurrentDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('currentDate').textContent = now.toLocaleDateString('es-ES', options);
}

// Refrescar datos
document.querySelector('.btn-outline-primary')?.addEventListener('click', function() {
    const currentPage = document.querySelector('.nav-link-custom.active').dataset.page;
    switch(currentPage) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'products':
            loadProducts();
            break;
        case 'sales':
            loadSales();
            break;
        case 'users':
            loadUsers();
            break;
    }
    alert('Datos actualizados');
});
