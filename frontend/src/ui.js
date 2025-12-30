export function showLoginPage() {
    document.getElementById('login-page').style.display = 'block';
    document.getElementById('main-system').style.display = 'none';
}

// Mapeo de roles a permisos (los nombres deben coincidir exactamente con los del backend)
const ROLE_PERMISSIONS = {
    'Administrador': ['dashboard', 'products', 'sales', 'purchases', 'users', 'reports', 'configuracion'],
    'Gerente': ['dashboard', 'products', 'sales', 'purchases', 'reports'],
    'Vendedor': ['dashboard', 'sales'],
    'Jefe de Bodega': ['dashboard', 'products', 'purchases'],
    'Contador': ['dashboard', 'reports'],
    'Vendedor Mayorista': ['dashboard', 'sales'],
    'Vendedor Minorista': ['dashboard', 'sales']
};

export function showMainSystem(userRole = 'Vendedor') {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('main-system').style.display = 'flex';
    
    // Obtener permisos según el rol o usar Vendedor como predeterminado
    const allowedPages = ROLE_PERMISSIONS[userRole] || ROLE_PERMISSIONS['Vendedor'];
    
    // Mostrar/ocultar elementos de navegación según permisos
    document.querySelectorAll('.nav-link-custom').forEach(link => {
        const page = link.dataset.page;
        if (page) {
            const shouldShow = allowedPages.includes(page);
            link.style.display = shouldShow ? 'flex' : 'none';
            
            // Si es la página de dashboard y está permitida, mostrarla por defecto
            if (page === 'dashboard' && shouldShow) {
                link.classList.add('active');
                document.getElementById('pageTitle').textContent = 'Dashboard';
            } else {
                link.classList.remove('active');
            }
        }
    });
    
    // Mostrar solo el contenido del dashboard inicialmente
    document.querySelectorAll('#pageContent > div').forEach(content => {
        content.style.display = content.id === 'dashboardPage' ? 'block' : 'none';
    });
}

export function updateUserInfo(user) {
    document.getElementById('userName').textContent = user.name;
    document.getElementById('userRole').textContent = user.role;
    document.getElementById('userAvatar').textContent = user.name.charAt(0).toUpperCase();
}

export function navigateTo(page) {
    // Verificar si la página solicitada está permitida para el rol del usuario
    const currentRole = document.getElementById('userRole').textContent;
    const allowedPages = ROLE_PERMISSIONS[currentRole] || [];
    
    if (!allowedPages.includes(page)) {
        console.warn(`Acceso no autorizado a la página: ${page}`);
        // Redirigir al dashboard si no tiene permiso
        if (allowedPages.includes('dashboard')) {
            page = 'dashboard';
        } else {
            // Si ni siquiera tiene acceso al dashboard, mostrar error
            alert('No tiene permisos para acceder a esta sección');
            return;
        }
    }
    
    // Actualizar la navegación
    document.querySelectorAll('.nav-link-custom').forEach(link => {
        link.classList.toggle('active', link.dataset.page === page);
    });
    
    // Mostrar solo el contenido de la página solicitada
    document.querySelectorAll('#pageContent > div').forEach(content => {
        content.style.display = content.id === `${page}Page` ? 'block' : 'none';
    });
    
    // Actualizar el título de la página
    const pageTitles = {
        'dashboard': 'Dashboard',
        'productos': 'Gestión de Productos',
        'ventas': 'Ventas',
        'compras': 'Compras',
        'usuarios': 'Gestión de Usuarios',
        'reportes': 'Reportes',
        'configuracion': 'Configuración'
    };
    
    document.getElementById('pageTitle').textContent = pageTitles[page] || page.charAt(0).toUpperCase() + page.slice(1);
    
    // Guardar la última página visitada (opcional, para mantener el estado)
    if (window.history && window.history.pushState) {
        window.history.pushState({ page }, '', `#${page}`);
    }
}

export function renderProducts(products) {
    const tableBody = document.getElementById('productsTable');
    tableBody.innerHTML = products.map(product => `
        <tr class="${product.stock_actual <= product.stock_minimo ? 'stock-warning' : ''}">
            <td>${product.codigo_producto}</td>
            <td>${product.nombre_producto}</td>
            <td>${product.nombre_categoria}</td>
            <td>${product.stock_actual}</td>
            <td>$${product.precio_venta.toFixed(2)}</td>
            <td><span class="badge bg-success">${product.estado}</span></td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" data-id="${product.id_producto}" data-action="edit-product">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" data-id="${product.id_producto}" data-action="delete-product">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

export function renderUsers(users) {
    const tableBody = document.getElementById('usersTable');
    tableBody.innerHTML = users.map(user => `
        <tr>
            <td>${user.usuario_login}</td>
            <td>${user.nombres} ${user.apellidos}</td>
            <td>${user.email}</td>
            <td><span class="badge role-${user.rol.toLowerCase().replace(' ', '-')}">${user.rol}</span></td>
            <td><span class="badge bg-success">${user.estado}</span></td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" data-id="${user.id_usuario}" data-action="edit-user">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" data-id="${user.id_usuario}" data-action="delete-user">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}
