import { login, logout } from './auth.js';
import { showMainSystem, showLoginPage, updateUserInfo, navigateTo, renderProducts, renderUsers } from './ui.js';
import apiRequest from './api.js';

let currentUser = null;

export async function handleLogin(event) {
    event.preventDefault();
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (!usernameInput || !passwordInput) {
        console.error('No se encontraron los campos de usuario o contraseña');
        return;
    }

    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    if (!username || !password) {
        alert('Por favor ingrese usuario y contraseña');
        return;
    }

    try {
        console.log('Iniciando sesión con:', username);
        currentUser = await login(username, password);
        console.log('Usuario autenticado:', currentUser);
        
        if (currentUser && currentUser.role) {
            showMainSystem(currentUser.role);
            updateUserInfo(currentUser);
            navigateTo('dashboard');
            loadDashboardData();
        } else {
            throw new Error('Datos de usuario incompletos');
        }
    } catch (error) {
        console.error('Error en handleLogin:', error);
        alert('Error de inicio de sesión: ' + (error.message || 'Credenciales incorrectas'));
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

function handleTestUserClick(event) {
    const userCard = event.target.closest('.user-card');
    if (!userCard) return;

    const username = userCard.dataset.username;
    const password = userCard.dataset.password;
    
    if (username && password) {
        document.getElementById('username').value = username;
        document.getElementById('password').value = password;
        
        // Optional: Auto-submit the form
        // document.getElementById('loginForm').dispatchEvent(new Event('submit'));
    }
}

export function setupEventHandlers() {
    // Login form handlers
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);
    
    // Navigation handler
    document.querySelector('.sidebar .nav')?.addEventListener('click', handleNavigation);
    
    // Test user click handler
    document.getElementById('test-users-container')?.addEventListener('click', handleTestUserClick);
}
