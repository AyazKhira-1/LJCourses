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
    html.setAttribute('data-bs-theme', newTheme);

    // Save to localStorage
    localStorage.setItem('theme', newTheme);
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
