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
        
        // Preparar el modal
        const modal = new bootstrap.Modal(document.getElementById('newProductModal'));
        const categorySelect = document.querySelector('#newProductModal select');
        
        // Limpiar y cargar categorías
        categorySelect.innerHTML = '<option value="">Seleccionar...</option>';
        categoriesResponse.categories.forEach(cat => {
            categorySelect.innerHTML += `<option value="${cat.id_categoria}">${cat.nombre_categoria}</option>`;
        });
        
        // Configurar el formulario
        const form = document.getElementById('productForm');
        form.reset();
        
        // Event listener para guardar
        const saveBtn = document.querySelector('#newProductModal .btn-primary');
        saveBtn.onclick = async function() {
            const formData = new FormData(form);
            const data = {
                codigo_producto: form[0].value,
                nombre_producto: form[1].value,
                precio_venta: parseFloat(form[2].value),
                stock_actual: parseInt(form[3].value),
                id_categoria: parseInt(categorySelect.value),
                id_proveedor: 1, // Valor por defecto, debería seleccionarse
                precio_compra_ref: parseFloat(form[2].value) * 0.7 // Estimado
            };
            
            // Validar datos
            const errors = validateProductForm(data);
            if (!showValidationErrors(errors)) {
                return; // Detener si hay errores
            }
            
            try {
                const response = await apiRequest('/products', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                
                if (response.success) {
                    showNotification('Producto creado correctamente', 'success');
                    modal.hide();
                    loadProducts(); // Recargar la lista
                }
            } catch (error) {
                const errorMessage = handleApiError(error, 'creación de producto');
                showNotification(errorMessage, 'danger');
            }
        };
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar creación de producto');
    }
}

// Función para crear nuevo usuario
async function createUser() {
    try {
        // Preparar el modal
        const modal = new bootstrap.Modal(document.getElementById('newUserModal'));
        const form = document.getElementById('userForm');
        form.reset();
        
        // Event listener para guardar
        const saveBtn = document.querySelector('#newUserModal .btn-primary');
        saveBtn.onclick = async function() {
            const roleMap = {
                'Administrador': 1,
                'Gerente': 2,
                'Jefe de Bodega': 3,
                'Vendedor': 4
            };
            
            const data = {
                nombres: form[0].value,
                apellidos: form[1].value,
                usuario_login: form[2].value,
                clave: form[3].value,
                id_tipo_usuario: roleMap[form[4].value],
                email: '', // Opcional
                telefono: '', // Opcional
                cedula: '' // Opcional
            };
            
            try {
                const response = await apiRequest('/users', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                
                if (response.success) {
                    alert('Usuario creado correctamente');
                    modal.hide();
                    loadUsers(); // Recargar la lista
                }
            } catch (error) {
                alert('Error al crear usuario: ' + error.message);
            }
        };
        
        modal.show();
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
        
        // Crear modal dinámicamente para nueva venta
        const modalHTML = `
            <div class="modal fade" id="newSaleModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header modal-header-custom">
                            <h5 class="modal-title text-white">Nueva Venta</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="saleForm">
                                <div class="mb-3">
                                    <label class="form-label">Cliente *</label>
                                    <select class="form-control" id="customerSelect" required>
                                        <option value="">Seleccionar cliente...</option>
                                        ${customersResponse.customers.map(c => 
                                            `<option value="${c.id_cliente}">${c.nombres} ${c.apellidos}</option>`
                                        ).join('')}
                                    </select>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Productos</label>
                                    <div id="saleProducts">
                                        <div class="row mb-2">
                                            <div class="col-md-5">
                                                <select class="form-control product-select">
                                                    <option value="">Seleccionar producto...</option>
                                                    ${productsResponse.products.map(p => 
                                                        `<option value="${p.id_producto}" data-price="${p.precio_venta}" data-stock="${p.stock_actual}">
                                                            ${p.nombre_producto} (Stock: ${p.stock_actual})
                                                        </option>`
                                                    ).join('')}
                                                </select>
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control quantity-input" placeholder="Cant." min="1">
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control price-input" placeholder="Precio" readonly>
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control subtotal-input" placeholder="Subtotal" readonly>
                                            </div>
                                            <div class="col-md-1">
                                                <button type="button" class="btn btn-danger btn-sm" onclick="removeSaleProduct(this)">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <button type="button" class="btn btn-outline-primary btn-sm mt-2" onclick="addSaleProduct()">
                                        <i class="fas fa-plus"></i> Agregar Producto
                                    </button>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <label class="form-label">Total:</label>
                                        <input type="number" class="form-control" id="saleTotal" readonly>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label">Tipo Comprobante:</label>
                                        <select class="form-control" id="receiptType">
                                            <option value="FACTURA">Factura</option>
                                            <option value="BOLETA">Boleta</option>
                                        </select>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-success" onclick="saveSale()">Guardar Venta</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('newSaleModal'));
        
        // Configurar eventos
        window.addSaleProduct = function() {
            const container = document.getElementById('saleProducts');
            const newProduct = container.querySelector('.row').cloneNode(true);
            newProduct.querySelectorAll('input').forEach(input => input.value = '');
            container.appendChild(newProduct);
        };
        
        window.removeSaleProduct = function(btn) {
            const rows = document.querySelectorAll('#saleProducts .row');
            if (rows.length > 1) {
                btn.closest('.row').remove();
                calculateSaleTotal();
            }
        };
        
        window.calculateSaleTotal = function() {
            let total = 0;
            document.querySelectorAll('#saleProducts .row').forEach(row => {
                const quantity = parseFloat(row.querySelector('.quantity-input').value) || 0;
                const price = parseFloat(row.querySelector('.price-input').value) || 0;
                const subtotal = quantity * price;
                row.querySelector('.subtotal-input').value = subtotal.toFixed(2);
                total += subtotal;
            });
            document.getElementById('saleTotal').value = total.toFixed(2);
        };
        
        // Event listeners para cálculos automáticos
        const saleModal = document.getElementById('newSaleModal');
        if (saleModal) {
            saleModal.addEventListener('change', function(e) {
                if (e.target.classList.contains('product-select')) {
                    const selected = e.target.options[e.target.selectedIndex];
                    const price = selected.dataset.price;
                    const stock = selected.dataset.stock;
                    const row = e.target.closest('.row');
                    row.querySelector('.price-input').value = price;
                    row.querySelector('.quantity-input').max = stock;
                    calculateSaleTotal();
                }
                if (e.target.classList.contains('quantity-input')) {
                    calculateSaleTotal();
                }
            });
        }
        
        window.saveSale = async function() {
            const customerId = document.getElementById('customerSelect').value;
            const receiptType = document.getElementById('receiptType').value;
            
            if (!customerId) {
                alert('Seleccione un cliente');
                return;
            }
            
            const detalles = [];
            document.querySelectorAll('#saleProducts .row').forEach(row => {
                const productId = row.querySelector('.product-select').value;
                const quantity = parseFloat(row.querySelector('.quantity-input').value);
                const price = parseFloat(row.querySelector('.price-input').value);
                
                if (productId && quantity > 0) {
                    detalles.push({
                        id_producto: parseInt(productId),
                        cantidad: quantity,
                        precio_unitario: price
                    });
                }
            });
            
            if (detalles.length === 0) {
                alert('Agregue al menos un producto');
                return;
            }
            
            try {
                const response = await apiRequest('/sales', {
                    method: 'POST',
                    body: JSON.stringify({
                        id_cliente: parseInt(customerId),
                        tipo_comprobante: receiptType,
                        detalles: detalles
                    })
                });
                
                if (response.success) {
                    alert(`Venta creada correctamente\nComprobante: ${response.numero_comprobante}\nTotal: $${response.total.toFixed(2)}`);
                    modal.hide();
                    loadSales(); // Recargar la lista
                    // Limpiar modal del DOM
                    document.getElementById('newSaleModal').remove();
                }
            } catch (error) {
                alert('Error al crear venta: ' + error.message);
            }
        };
        
        modal.show();
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
async function editProduct(id) {
    try {
        // Obtener datos del producto
        const response = await apiRequest('/products');
        const product = response.products.find(p => p.id_producto === id);
        
        if (!product) {
            alert('Producto no encontrado');
            return;
        }
        
        // Obtener categorías y proveedores
        const [categoriesResponse, providersResponse] = await Promise.all([
            apiRequest('/categories'),
            apiRequest('/providers')
        ]);
        
        // Preparar el modal
        const modal = new bootstrap.Modal(document.getElementById('newProductModal'));
        const categorySelect = document.querySelector('#newProductModal select');
        
        // Cambiar título del modal
        document.querySelector('#newProductModal .modal-title').textContent = 'Editar Producto';
        
        // Cargar categorías
        categorySelect.innerHTML = '<option value="">Seleccionar...</option>';
        categoriesResponse.categories.forEach(cat => {
            const selected = cat.id_categoria === product.id_categoria ? 'selected' : '';
            categorySelect.innerHTML += `<option value="${cat.id_categoria}" ${selected}>${cat.nombre_categoria}</option>`;
        });
        
        // Llenar formulario con datos del producto
        const form = document.getElementById('productForm');
        form[0].value = product.codigo_producto;
        form[1].value = product.nombre_producto;
        form[2].value = product.precio_venta;
        form[3].value = product.stock_actual;
        
        // Event listener para actualizar
        const saveBtn = document.querySelector('#newProductModal .btn-primary');
        saveBtn.onclick = async function() {
            const data = {
                codigo_producto: form[0].value,
                nombre_producto: form[1].value,
                precio_venta: parseFloat(form[2].value),
                stock_actual: parseInt(form[3].value),
                id_categoria: parseInt(categorySelect.value),
                id_proveedor: product.id_proveedor,
                precio_compra_ref: product.precio_compra_ref
            };
            
            try {
                const response = await apiRequest(`/products/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                
                if (response.success) {
                    alert('Producto actualizado correctamente');
                    modal.hide();
                    loadProducts();
                }
            } catch (error) {
                alert('Error al actualizar producto: ' + error.message);
            }
        };
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar edición de producto');
    }
}

async function deleteProduct(id) {
    if (confirm('¿Está seguro de eliminar este producto?')) {
        try {
            const response = await apiRequest(`/products/${id}`, {
                method: 'DELETE'
            });
            
            if (response.success) {
                alert('Producto eliminado correctamente');
                loadProducts();
            }
        } catch (error) {
            alert('Error al eliminar producto: ' + error.message);
        }
    }
}

async function editUser(id) {
    try {
        // Obtener datos del usuario
        const response = await apiRequest('/users');
        const user = response.users.find(u => u.id_usuario === id);
        
        if (!user) {
            alert('Usuario no encontrado');
            return;
        }
        
        // Preparar el modal
        const modal = new bootstrap.Modal(document.getElementById('newUserModal'));
        
        // Cambiar título del modal
        document.querySelector('#newUserModal .modal-title').textContent = 'Editar Usuario';
        
        // Llenar formulario con datos del usuario
        const form = document.getElementById('userForm');
        const names = user.nombres.split(' ');
        const surnames = user.apellidos.split(' ');
        form[0].value = names[0] || '';
        form[1].value = surnames[0] || '';
        form[2].value = user.usuario_login;
        form[3].value = ''; // No mostrar contraseña actual
        form[4].value = user.rol;
        
        // Event listener para actualizar
        const saveBtn = document.querySelector('#newUserModal .btn-primary');
        saveBtn.onclick = async function() {
            const roleMap = {
                'Administrador': 1,
                'Gerente': 2,
                'Jefe de Bodega': 3,
                'Vendedor': 4
            };
            
            const data = {
                nombres: form[0].value,
                apellidos: form[1].value,
                usuario_login: form[2].value,
                id_tipo_usuario: roleMap[form[4].value],
                email: user.email,
                telefono: user.telefono,
                cedula: user.cedula
            };
            
            // Solo incluir contraseña si se ingresó una nueva
            if (form[3].value) {
                data.clave = form[3].value;
            }
            
            try {
                const response = await apiRequest(`/users/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                
                if (response.success) {
                    alert('Usuario actualizado correctamente');
                    modal.hide();
                    loadUsers();
                }
            } catch (error) {
                alert('Error al actualizar usuario: ' + error.message);
            }
        };
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar edición de usuario');
    }
}

async function deleteUser(id) {
    if (confirm('¿Está seguro de eliminar este usuario?')) {
        try {
            const response = await apiRequest(`/users/${id}`, {
                method: 'DELETE'
            });
            
            if (response.success) {
                alert('Usuario eliminado correctamente');
                loadUsers();
            }
        } catch (error) {
            alert('Error al eliminar usuario: ' + error.message);
        }
    }
}

async function viewSale(id) {
    try {
        // Obtener detalles de la venta
        const salesResponse = await apiRequest('/sales');
        const sale = salesResponse.sales.find(s => s.id_venta === id);
        
        if (!sale) {
            alert('Venta no encontrada');
            return;
        }
        
        // Crear modal para ver detalles
        const modalHTML = `
            <div class="modal fade" id="viewSaleModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header modal-header-custom">
                            <h5 class="modal-title text-white">Detalles de Venta</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Comprobante:</strong> ${sale.numero_comprobante}
                                </div>
                                <div class="col-md-6">
                                    <strong>Fecha:</strong> ${new Date(sale.fecha_hora).toLocaleString()}
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Cliente:</strong> ${sale.cliente_nombre} ${sale.cliente_apellido}
                                </div>
                                <div class="col-md-6">
                                    <strong>Vendedor:</strong> ${sale.vendedor_nombre} ${sale.vendedor_apellido}
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Estado:</strong> <span class="badge bg-success">${sale.estado}</span>
                                </div>
                                <div class="col-md-6">
                                    <strong>Total:</strong> $${sale.total.toFixed(2)}
                                </div>
                            </div>
                            <hr>
                            <h6>Productos Vendidos</h6>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Producto</th>
                                            <th>Cantidad</th>
                                            <th>Precio Unit.</th>
                                            <th>Subtotal</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Aquí se cargarían los detalles de la venta -->
                                        <tr>
                                            <td colspan="4" class="text-center">Detalles no disponibles</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('viewSaleModal'));
        
        // Eliminar modal del DOM al cerrar
        document.getElementById('viewSaleModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar detalles de venta');
    }
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
                case 'purchases':
                    loadPurchases();
                    break;
            }
        }
    });
});

// Event listener para logout
document.getElementById('logoutBtn').addEventListener('click', logout);

// Event listeners para botones de creación
document.addEventListener('DOMContentLoaded', function() {
    // Asignar event listeners de forma segura
    const newProductBtn = document.getElementById('newProductBtn');
    if (newProductBtn) {
        newProductBtn.addEventListener('click', createProduct);
    }
    
    const newUserBtn = document.getElementById('newUserBtn');
    if (newUserBtn) {
        newUserBtn.addEventListener('click', createUser);
    }
    
    const newSaleBtn = document.getElementById('newSaleBtn');
    if (newSaleBtn) {
        newSaleBtn.addEventListener('click', createSale);
    }
    
    const newPurchaseBtn = document.getElementById('newPurchaseBtn');
    if (newPurchaseBtn) {
        newPurchaseBtn.addEventListener('click', createPurchase);
    }
    
    // Refrescar datos
    const refreshBtn = document.querySelector('.btn-outline-primary');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
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
                case 'purchases':
                    loadPurchases();
                    break;
            }
            alert('Datos actualizados');
        });
    }
});

// ============== FUNCIONES DE VALIDACIÓN ==============

// Función para validar formulario de producto
function validateProductForm(formData) {
    const errors = [];
    
    if (!formData.codigo_producto || formData.codigo_producto.trim() === '') {
        errors.push('El código del producto es requerido');
    }
    
    if (!formData.nombre_producto || formData.nombre_producto.trim() === '') {
        errors.push('El nombre del producto es requerido');
    }
    
    if (!formData.precio_venta || formData.precio_venta <= 0) {
        errors.push('El precio de venta debe ser mayor a 0');
    }
    
    if (!formData.stock_actual || formData.stock_actual < 0) {
        errors.push('El stock no puede ser negativo');
    }
    
    if (!formData.id_categoria) {
        errors.push('Debe seleccionar una categoría');
    }
    
    return errors;
}

// Función para validar formulario de usuario
function validateUserForm(formData) {
    const errors = [];
    
    if (!formData.nombres || formData.nombres.trim() === '') {
        errors.push('Los nombres son requeridos');
    }
    
    if (!formData.apellidos || formData.apellidos.trim() === '') {
        errors.push('Los apellidos son requeridos');
    }
    
    if (!formData.usuario_login || formData.usuario_login.trim() === '') {
        errors.push('El usuario de login es requerido');
    }
    
    if (formData.usuario_login && formData.usuario_login.length < 3) {
        errors.push('El usuario de login debe tener al menos 3 caracteres');
    }
    
    if (!formData.clave || formData.clave.length < 4) {
        errors.push('La contraseña debe tener al menos 4 caracteres');
    }
    
    if (!formData.id_tipo_usuario) {
        errors.push('Debe seleccionar un rol');
    }
    
    return errors;
}

// Función para mostrar errores de validación
function showValidationErrors(errors) {
    if (errors.length > 0) {
        alert('Errores de validación:\n\n' + errors.join('\n'));
        return false;
    }
    return true;
}

// ============== MANEJO DE ERRORES MEJORADO ==============

// Función para manejar errores de API de forma más amigable
function handleApiError(error, context = '') {
    console.error(`Error en ${context}:`, error);
    
    let userMessage = 'Ha ocurrido un error inesperado';
    
    if (error.message) {
        if (error.message.includes('Network') || error.message.includes('fetch')) {
            userMessage = 'Error de conexión. Verifique su conexión a internet.';
        } else if (error.message.includes('401')) {
            userMessage = 'No autorizado. Inicie sesión nuevamente.';
        } else if (error.message.includes('403')) {
            userMessage = 'No tiene permisos para realizar esta acción.';
        } else if (error.message.includes('404')) {
            userMessage = 'El recurso solicitado no fue encontrado.';
        } else if (error.message.includes('500')) {
            userMessage = 'Error del servidor. Intente nuevamente más tarde.';
        } else {
            userMessage = error.message;
        }
    }
    
    return userMessage;
}

// Función para mostrar notificaciones en lugar de alerts
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// ============== FUNCIONES AUXILIARES ==============

// Actualizar fecha actual
function updateCurrentDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('es-ES', options);
    }
}

// Actualizar fecha cada minuto
setInterval(updateCurrentDate, 60000);

// ============== FUNCIÓN DE COMPRA ==============

// Función para cargar compras
async function loadPurchases() {
    try {
        const response = await apiRequest('/purchases');
        const purchases = response.purchases || [];
        
        let purchasesHTML = '';
        purchases.forEach(purchase => {
            const statusClass = purchase.estado === 'COMPLETADA' ? 'bg-success' : 'bg-warning';
            purchasesHTML += `
                <tr>
                    <td>${purchase.numero_comprobante}</td>
                    <td>${new Date(purchase.fecha_hora).toLocaleDateString()}</td>
                    <td>${purchase.nombre_proveedor || 'Proveedor'}</td>
                    <td>$${purchase.total.toFixed(2)}</td>
                    <td><span class="badge ${statusClass}">${purchase.estado}</span></td>
                    <td>
                        <button class="btn btn-sm btn-info btn-action" onclick="viewPurchase(${purchase.id_compra})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        document.getElementById('purchasesTable').innerHTML = purchasesHTML || '<tr><td colspan="6" class="text-center text-muted"><i class="fas fa-info-circle"></i> No hay compras registradas</td></tr>';
    } catch (error) {
        console.error('Error cargando compras:', error);
        document.getElementById('purchasesTable').innerHTML = '<tr><td colspan="6" class="text-center">Error al cargar compras</td></tr>';
    }
}

// Función para ver detalles de compra
async function viewPurchase(id) {
    try {
        // Obtener detalles de la compra
        const purchasesResponse = await apiRequest('/purchases');
        const purchase = purchasesResponse.purchases.find(p => p.id_compra === id);
        
        if (!purchase) {
            alert('Compra no encontrada');
            return;
        }
        
        // Crear modal para ver detalles
        const modalHTML = `
            <div class="modal fade" id="viewPurchaseModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header modal-header-custom">
                            <h5 class="modal-title text-white">Detalles de Compra</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Comprobante:</strong> ${purchase.numero_comprobante}
                                </div>
                                <div class="col-md-6">
                                    <strong>Fecha:</strong> ${new Date(purchase.fecha_hora).toLocaleString()}
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Proveedor:</strong> ${purchase.nombre_proveedor || 'N/A'}
                                </div>
                                <div class="col-md-6">
                                    <strong>Estado:</strong> <span class="badge bg-success">${purchase.estado}</span>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <strong>Total:</strong> $${purchase.total.toFixed(2)}
                                </div>
                            </div>
                            <hr>
                            <h6>Productos Comprados</h6>
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Producto</th>
                                            <th>Cantidad</th>
                                            <th>Precio Unit.</th>
                                            <th>Subtotal</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Aquí se cargarían los detalles de la compra -->
                                        <tr>
                                            <td colspan="4" class="text-center">Detalles no disponibles</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('viewPurchaseModal'));
        
        // Eliminar modal del DOM al cerrar
        document.getElementById('viewPurchaseModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar detalles de compra');
    }
}

// Función para crear nueva compra
async function createPurchase() {
    try {
        // Obtener proveedores y productos
        const [providersResponse, productsResponse] = await Promise.all([
            apiRequest('/providers'),
            apiRequest('/products')
        ]);
        
        // Crear modal dinámicamente para nueva compra
        const modalHTML = `
            <div class="modal fade" id="newPurchaseModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header modal-header-custom">
                            <h5 class="modal-title text-white">Nueva Compra</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="purchaseForm">
                                <div class="mb-3">
                                    <label class="form-label">Proveedor *</label>
                                    <select class="form-control" id="providerSelect" required>
                                        <option value="">Seleccionar proveedor...</option>
                                        ${providersResponse.providers ? providersResponse.providers.map(p => 
                                            `<option value="${p.id_proveedor}">${p.nombre_proveedor}</option>`
                                        ).join('') : '<option value="1">Proveedor General</option>'}
                                    </select>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Productos</label>
                                    <div id="purchaseProducts">
                                        <div class="row mb-2">
                                            <div class="col-md-5">
                                                <select class="form-control product-select">
                                                    <option value="">Seleccionar producto...</option>
                                                    ${productsResponse.products.map(p => 
                                                        `<option value="${p.id_producto}" data-price="${p.precio_compra_ref || p.precio_venta * 0.7}">
                                                            ${p.nombre_producto}
                                                        </option>`
                                                    ).join('')}
                                                </select>
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control quantity-input" placeholder="Cant." min="1">
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control price-input" placeholder="Precio" step="0.01">
                                            </div>
                                            <div class="col-md-2">
                                                <input type="number" class="form-control subtotal-input" placeholder="Subtotal" readonly>
                                            </div>
                                            <div class="col-md-1">
                                                <button type="button" class="btn btn-danger btn-sm" onclick="removePurchaseProduct(this)">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <button type="button" class="btn btn-outline-primary btn-sm mt-2" onclick="addPurchaseProduct()">
                                        <i class="fas fa-plus"></i> Agregar Producto
                                    </button>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6">
                                        <label class="form-label">Total:</label>
                                        <input type="number" class="form-control" id="purchaseTotal" readonly>
                                    </div>
                                    <div class="col-md-6">
                                        <label class="form-label">Tipo Comprobante:</label>
                                        <select class="form-control" id="purchaseReceiptType">
                                            <option value="FACTURA">Factura</option>
                                            <option value="BOLETA">Boleta</option>
                                        </select>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-success" onclick="savePurchase()">Guardar Compra</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Agregar modal al DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('newPurchaseModal'));
        
        // Configurar eventos
        window.addPurchaseProduct = function() {
            const container = document.getElementById('purchaseProducts');
            const newProduct = container.querySelector('.row').cloneNode(true);
            newProduct.querySelectorAll('input').forEach(input => input.value = '');
            container.appendChild(newProduct);
        };
        
        window.removePurchaseProduct = function(btn) {
            const rows = document.querySelectorAll('#purchaseProducts .row');
            if (rows.length > 1) {
                btn.closest('.row').remove();
                calculatePurchaseTotal();
            }
        };
        
        window.calculatePurchaseTotal = function() {
            let total = 0;
            document.querySelectorAll('#purchaseProducts .row').forEach(row => {
                const quantity = parseFloat(row.querySelector('.quantity-input').value) || 0;
                const price = parseFloat(row.querySelector('.price-input').value) || 0;
                const subtotal = quantity * price;
                row.querySelector('.subtotal-input').value = subtotal.toFixed(2);
                total += subtotal;
            });
            document.getElementById('purchaseTotal').value = total.toFixed(2);
        };
        
        // Event listeners para cálculos automáticos
        const purchaseModal = document.getElementById('newPurchaseModal');
        if (purchaseModal) {
            purchaseModal.addEventListener('change', function(e) {
                if (e.target.classList.contains('product-select')) {
                    const selected = e.target.options[e.target.selectedIndex];
                    const price = selected.dataset.price || 0;
                    const row = e.target.closest('.row');
                    row.querySelector('.price-input').value = parseFloat(price).toFixed(2);
                    calculatePurchaseTotal();
                }
                if (e.target.classList.contains('quantity-input') || e.target.classList.contains('price-input')) {
                    calculatePurchaseTotal();
                }
            });
        }
        
        window.savePurchase = async function() {
            const providerId = document.getElementById('providerSelect').value;
            const receiptType = document.getElementById('purchaseReceiptType').value;
            
            if (!providerId) {
                alert('Seleccione un proveedor');
                return;
            }
            
            const detalles = [];
            document.querySelectorAll('#purchaseProducts .row').forEach(row => {
                const productId = row.querySelector('.product-select').value;
                const quantity = parseFloat(row.querySelector('.quantity-input').value);
                const price = parseFloat(row.querySelector('.price-input').value);
                
                if (productId && quantity > 0 && price > 0) {
                    detalles.push({
                        id_producto: parseInt(productId),
                        cantidad: quantity,
                        precio_unitario: price
                    });
                }
            });
            
            if (detalles.length === 0) {
                alert('Agregue al menos un producto');
                return;
            }
            
            try {
                const response = await apiRequest('/purchases', {
                    method: 'POST',
                    body: JSON.stringify({
                        id_proveedor: parseInt(providerId),
                        tipo_comprobante: receiptType,
                        detalles: detalles
                    })
                });
                
                if (response.success) {
                    alert(`Compra registrada correctamente\nComprobante: ${response.numero_comprobante}\nTotal: $${response.total.toFixed(2)}`);
                    modal.hide();
                    // Limpiar modal del DOM
                    document.getElementById('newPurchaseModal').remove();
                }
            } catch (error) {
                alert('Error al registrar compra: ' + error.message);
            }
        };
        
        modal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Error al preparar creación de compra');
    }
}

// ============== REPORTES ==============

// Función para generar reportes
async function generateReport(type) {
    try {
        let data = [];
        let filename = '';
        let title = '';
        
        switch(type) {
            case 'products':
                const productsResponse = await apiRequest('/products');
                data = productsResponse.products;
                filename = 'reporte_productos';
                title = 'Reporte de Productos';
                break;
            case 'sales':
                const salesResponse = await apiRequest('/sales');
                data = salesResponse.sales;
                filename = 'reporte_ventas';
                title = 'Reporte de Ventas';
                break;
            case 'stock':
                const stockResponse = await apiRequest('/dashboard/low-stock');
                data = stockResponse.products;
                filename = 'reporte_stock_bajo';
                title = 'Reporte de Stock Bajo';
                break;
        }
        
        if (!data || data.length === 0) {
            alert('No hay datos disponibles para generar el reporte');
            return;
        }
        
        // Generar CSV simple (puedes mejorar esto para PDF)
        let csvContent = title + '\n\n';
        
        if (type === 'products') {
            csvContent += 'Código,Producto,Categoría,Stock,Precio\n';
            data.forEach(item => {
                csvContent += `${item.codigo_producto},${item.nombre_producto},${item.nombre_categoria},${item.stock_actual},${item.precio_venta}\n`;
            });
        } else if (type === 'sales') {
            csvContent += 'Comprobante,Fecha,Cliente,Total,Vendedor,Estado\n';
            data.forEach(item => {
                csvContent += `${item.numero_comprobante},${new Date(item.fecha_hora).toLocaleDateString()},${item.cliente_nombre} ${item.cliente_apellido},${item.total},${item.vendedor_nombre} ${item.vendedor_apellido},${item.estado}\n`;
            });
        } else if (type === 'stock') {
            csvContent += 'Código,Producto,Stock Actual,Stock Mínimo\n';
            data.forEach(item => {
                csvContent += `${item.codigo_producto},${item.nombre_producto},${item.stock_actual},${item.stock_minimo}\n`;
            });
        }
        
        // Descargar archivo
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename + '.csv');
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        alert(`Reporte '${title}' generado correctamente`);
    } catch (error) {
        console.error('Error generando reporte:', error);
        alert('Error al generar reporte: ' + error.message);
    }
}
