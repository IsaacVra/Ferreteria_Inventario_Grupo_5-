import { login, logout } from './auth.js';
import { showMainSystem, showLoginPage, updateUserInfo, navigateTo, renderProducts, renderUsers } from './ui.js';
import apiRequest, { getTestUsers } from './api.js';

let currentUser = null;

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        currentUser = await login(username, password);
        showMainSystem();
        updateUserInfo(currentUser);
        navigateTo('dashboard');
        loadDashboardData();
    } catch (error) {
        alert('Error de login: ' + error.message);
    }
}

async function handleLogout() {
    try {
        await logout();
        currentUser = null;
        showLoginPage();
    } catch (error) {
        console.error('Error en logout:', error);
        location.reload();
    }
}

function handleNavigation(event) {
    event.preventDefault();
    const page = event.target.dataset.page;
    if (page) {
        navigateTo(page);
        loadPageData(page);
    }
}

async function loadDashboardData() {
    try {
        const { stats } = await apiRequest('/dashboard/stats');
        document.getElementById('totalProducts').textContent = stats.total_products;
        document.getElementById('totalUsers').textContent = stats.total_users;
        document.getElementById('todaySales').textContent = `$${stats.today_sales_amount.toFixed(2)}`;
        document.getElementById('inventoryValue').textContent = `$${stats.inventory_value.toFixed(2)}`;
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadPageData(page) {
    switch (page) {
        case 'products':
            const { products } = await apiRequest('/products');
            renderProducts(products);
            break;
        case 'users':
            const { users } = await apiRequest('/users');
            renderUsers(users);
            break;
        // Add cases for other pages (sales, purchases, etc.)
    }
}

// Renderizar usuarios de prueba
async function renderTestUsers() {
    try {
        const testUsers = await getTestUsers();
        const container = document.getElementById('test-users-container');
        
        if (!container) return;
        
        // Limpiar contenedor
        container.innerHTML = '<h4 class="mb-4">Usuarios para Prueba</h4>';
        
        // Crear tarjetas para cada usuario
        testUsers.forEach(user => {
            const userCard = document.createElement('div');
            userCard.className = 'user-card mb-3 p-3 border rounded';
            userCard.style.cursor = 'pointer';
            userCard.dataset.username = user.username;
            
            // Determinar el color del badge según el rol
            let badgeClass = 'badge bg-secondary';
            if (user.role.toLowerCase() === 'admin') badgeClass = 'badge bg-danger';
            else if (user.role.toLowerCase() === 'gerente') badgeClass = 'badge bg-primary';
            else if (user.role.toLowerCase() === 'bodega') badgeClass = 'badge bg-warning';
            else if (user.role.toLowerCase() === 'vendedor') badgeClass = 'badge bg-success';
            
            userCard.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong><i class="fas fa-user"></i> ${user.name}</strong>
                        <div class="user-role">${user.role}</div>
                    </div>
                    <div>
                        <span class="${badgeClass}">${user.role}</span>
                    </div>
                </div>
                <div class="mt-2">
                    <small><strong>Usuario:</strong> ${user.username}</small>
                </div>
            `;
            
            // Agregar manejador de eventos
            userCard.addEventListener('click', handleTestUserClick);
            container.appendChild(userCard);
        });
    } catch (error) {
        console.error('Error cargando usuarios de prueba:', error);
    }
}

function handleTestUserClick(event) {
    event.preventDefault();
    const card = event.currentTarget;
    const username = card.dataset.username;
    let password = '';

    // Obtener el rol del badge
    const badge = card.querySelector('.badge');
    if (!badge) return;

    const role = badge.textContent.trim().toLowerCase();
    
    // Asignar contraseña basada en el rol (usando includes para mayor flexibilidad)
    if (role.includes('admin')) password = 'admin123';
    else if (role.includes('gerente')) password = 'gerente123';
    else if (role.includes('bodega')) password = 'bodega123';
    else if (role.includes('vendedor')) password = 'ventas123';
    
    // Rellenar los campos del formulario
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (usernameInput && passwordInput) {
        usernameInput.value = username;
        passwordInput.value = password;
        
        // Enfocar el campo de contraseña para facilitar el inicio de sesión
        passwordInput.focus();
        
        // Mostrar un mensaje de depuración en consola
        console.log(`Usuario: ${username}, Contraseña: ${'*'.repeat(password.length)}`);
    }
}

export async function setupEventHandlers() {
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
    document.querySelector('.sidebar .nav').addEventListener('click', handleNavigation);
    
    // Cargar usuarios de prueba al iniciar
    await renderTestUsers();
}
