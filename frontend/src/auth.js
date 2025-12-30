import apiRequest from './api.js';

export async function login(username, password) {
    const response = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });
    return response.user;
}

export async function logout() {
    await apiRequest('/api/auth/logout', { method: 'POST' });
}

export async function getCurrentUser() {
    try {
        const response = await apiRequest('/api/auth/me');
        return response.user;
    } catch (error) {
        if (error.message.includes('No autenticado')) {
            return null;
        }
        throw error;
    }
}
