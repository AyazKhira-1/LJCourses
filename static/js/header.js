// ============================================
// HEADER LOGOUT FUNCTIONALITY
// ============================================

/**
 * Handle logout
 */
function handleLogout(event) {
    if (event) {
        event.preventDefault();
    }

    // Clear all localStorage data
    localStorage.clear();

    // Redirect to home page
    window.location.href = '/';
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
