// ============================================
// SIGN-UP PAGE SPECIFIC JAVASCRIPT
// ============================================

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';
    toast.textContent = message;

    document.body.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Initialize sign-up page functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    // Google Sign Up Button Handler
    const googleSignUpBtn = document.querySelector('.google-icon');
    if (googleSignUpBtn && googleSignUpBtn.closest('button')) {
        googleSignUpBtn.closest('button').addEventListener('click', function (e) {
            e.preventDefault();

            showNotification(
                'Google OAuth integration coming soon. This will redirect to Google authentication.',
                'info'
            );

            // Production: Redirect to Google OAuth
            // window.location.href = '/auth/google';
        });
    }

    // Password visibility toggle
    const passwordToggles = document.querySelectorAll('.form-icon-right.clickable');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            try {
                const input = this.parentElement.querySelector('input');
                if (input && input.type === 'password') {
                    input.type = 'text';
                    this.textContent = 'visibility';
                } else if (input) {
                    input.type = 'password';
                    this.textContent = 'visibility_off';
                }
            } catch (error) {
                showNotification('Error toggling password visibility', 'danger');
            }
        });
    });
});
