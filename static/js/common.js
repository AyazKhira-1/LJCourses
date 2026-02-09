// ============================================
// COMMON JAVASCRIPT - SHARED ACROSS ALL PAGES
// ============================================

/**
 * Toggle between light and dark theme
 */
function toggleDarkMode() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    setTheme(newTheme);
}

/**
 * Set specific theme
 * @param {string} theme - 'light' or 'dark'
 */
function setTheme(theme) {
    const html = document.documentElement;
    html.setAttribute('data-bs-theme', theme);
    localStorage.setItem('theme', theme);

    // Dispatch event for other components to listen
    const event = new CustomEvent('themeChanged', { detail: { theme: theme } });
    document.dispatchEvent(event);
}

/**
 * Initialize theme on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Get the saved theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Apply the theme
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
});
