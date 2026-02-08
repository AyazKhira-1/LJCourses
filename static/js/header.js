// ============================================
// HEADER LOGOUT FUNCTIONALITY
// ============================================

/**
 * Handle logout
 */
async function handleLogout(event) {
    if (event) {
        event.preventDefault();
    }

    try {
        // Get the access token from localStorage
        const token = localStorage.getItem('access_token');

        if (token) {
            // Call the logout API to set is_active = False
            await fetch('http://127.0.0.1:8000/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.error('Logout API call failed:', error);
        // Continue with logout even if API call fails
    } finally {
        // Clear all localStorage data
        localStorage.clear();

        // Redirect to home page
        window.location.href = '/';
    }
}

/**
 * Initialize logout buttons
 */
document.addEventListener('DOMContentLoaded', () => {
    // Setup logout buttons
    const logoutButtons = document.querySelectorAll('[data-action="logout"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', handleLogout);
    });
});
