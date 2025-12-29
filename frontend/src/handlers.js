import { login, logout } from './auth.js';
import { showMainSystem, showLoginPage, updateUserInfo, navigateTo, renderProducts, renderUsers } from './ui.js';
import apiRequest from './api.js';

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

export function setupEventHandlers() {
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);
    document.querySelector('.sidebar .nav')?.addEventListener('click', handleNavigation);
}
