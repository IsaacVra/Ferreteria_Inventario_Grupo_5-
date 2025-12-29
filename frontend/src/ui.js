export function showLoginPage() {
    document.getElementById('login-page').style.display = 'block';
    document.getElementById('main-system').style.display = 'none';
}

export function showMainSystem() {
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('main-system').style.display = 'flex';
}

export function updateUserInfo(user) {
    document.getElementById('userName').textContent = user.name;
    document.getElementById('userRole').textContent = user.role;
    document.getElementById('userAvatar').textContent = user.name.charAt(0).toUpperCase();
}

export function navigateTo(page) {
    document.querySelectorAll('.nav-link-custom').forEach(link => {
        link.classList.toggle('active', link.dataset.page === page);
    });
    document.querySelectorAll('#pageContent > div').forEach(content => {
        content.style.display = content.id === `${page}Page` ? 'block' : 'none';
    });
    document.getElementById('pageTitle').textContent = page.charAt(0).toUpperCase() + page.slice(1);
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
