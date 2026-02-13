// ============================================
// LOGIN PAGE SPECIFIC JAVASCRIPT
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
 * Validate email format: enrollmentnumber@mail.ljku.edu.in
 * Enrollment number must be exactly 14 digits
 */
function validateEmail(email) {
    // Regular expression to match 14 digits followed by @mail.ljku.edu.in
    const emailPattern = /^(\d{14})@mail\.ljku\.edu\.in$/;
    const match = email.match(emailPattern);

    if (!match) {
        return {
            valid: false,
            message: 'Email must be in format: {14-digit-enrollment-number}@mail.ljku.edu.in'
        };
    }

    return {
        valid: true,
        enrollmentNumber: match[1]
    };
}

/**
 * Handle login form submission
 */
async function handleLoginSubmit(event) {
    event.preventDefault();

    // Get form values
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    // Validate email
    const emailValidation = validateEmail(email);
    if (!emailValidation.valid) {
        showNotification(emailValidation.message, 'danger');
        return;
    }

    // Validate password is not empty
    if (!password) {
        showNotification('Please enter your password', 'danger');
        return;
    }

    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Logging In...';

    try {
        const response = await fetch('/student-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        // 1. Handle JSON response with redirect (New optimized way)
        if (response.headers.get('content-type')?.includes('application/json')) {
            const data = await response.json();

            if (response.ok && data.success) {
                showNotification('Login successful! Redirecting...', 'success');
                window.location.href = data.redirect_url;
                return;
            } else {
                throw new Error(data.detail || 'Login failed');
            }
        }

        // 2. Fallback for unexpected HTML response (e.g. 500 server error)
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        // Should not reach here if backend correctly returns JSON
        window.location.reload();

    } catch (error) {
        console.error('Login error:', error);
        showNotification(error.message || 'Login failed', 'danger');
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
}

/**
 * Initialize login page functionality
 */
document.addEventListener('DOMContentLoaded', () => {
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

    // Handle form submission
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }

    // Real-time email validation feedback
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function () {
            const email = this.value.trim();
            if (email) {
                const validation = validateEmail(email);
                if (!validation.valid) {
                    this.classList.add('is-invalid');
                    showNotification(validation.message, 'warning');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            }
        });

        // Remove validation classes on focus
        emailInput.addEventListener('focus', function () {
            this.classList.remove('is-invalid', 'is-valid');
        });
    }
});
