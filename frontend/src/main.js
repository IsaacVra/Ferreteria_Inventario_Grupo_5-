import { setupEventHandlers } from './handlers.js';
import { getCurrentUser } from './auth.js';
import { showLoginPage, showMainSystem, updateUserInfo, navigateTo } from './ui.js';

document.addEventListener('DOMContentLoaded', async () => {
    setupEventHandlers();

    try {
        const user = await getCurrentUser();
        if (user) {
            showMainSystem();
            updateUserInfo(user);
            navigateTo('dashboard');
        } else {
            showLoginPage();
        }
    } catch (error) {
        console.error('Initialization error:', error);
        showLoginPage();
    }
});

