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
 * Validate password
 * Requirements:
 * - At least 8 characters long
 * - Include uppercase and lowercase letters
 * - Include at least one number
 * - Include at least one special character
 */
function validatePassword(password) {
    if (password.length < 8) {
        return {
            valid: false,
            message: 'Password must be at least 8 characters long'
        };
    }

    if (!/[A-Z]/.test(password)) {
        return {
            valid: false,
            message: 'Password must include at least one uppercase letter'
        };
    }

    if (!/[a-z]/.test(password)) {
        return {
            valid: false,
            message: 'Password must include at least one lowercase letter'
        };
    }

    if (!/[0-9]/.test(password)) {
        return {
            valid: false,
            message: 'Password must include at least one number'
        };
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        return {
            valid: false,
            message: 'Password must include at least one special character'
        };
    }

    return { valid: true };
}

/**
 * Validate passwords match
 */
function validatePasswordsMatch(password, confirmPassword) {
    if (password !== confirmPassword) {
        return {
            valid: false,
            message: 'Passwords do not match'
        };
    }

    return { valid: true };
}

/**
 * Handle form submission
 */
async function handleSignUpSubmit(event) {
    event.preventDefault();

    // Get form values
    const fullName = document.getElementById('fullname').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const termsCheckbox = document.getElementById('terms');

    // Validate full name
    if (!fullName) {
        showNotification('Please enter your full name', 'danger');
        return;
    }

    // Validate email
    const emailValidation = validateEmail(email);
    if (!emailValidation.valid) {
        showNotification(emailValidation.message, 'danger');
        return;
    }

    // Validate password
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.valid) {
        showNotification(passwordValidation.message, 'danger');
        return;
    }

    // Validate passwords match
    const passwordsMatchValidation = validatePasswordsMatch(password, confirmPassword);
    if (!passwordsMatchValidation.valid) {
        showNotification(passwordsMatchValidation.message, 'danger');
        return;
    }

    // Validate terms and conditions
    if (!termsCheckbox.checked) {
        showNotification('Please accept the Terms of Service and Privacy Policy', 'danger');
        return;
    }

    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Creating Account...';

    try {
        const response = await fetch('/student-sign-up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password,
                confirm_password: confirmPassword
            })
        });

        // 1. Handle JSON response with redirect (New optimized way)
        if (response.headers.get('content-type')?.includes('application/json')) {
            const data = await response.json();

            if (response.ok && data.success) {
                showNotification('Account created successfully! Redirecting...', 'success');
                window.location.href = data.redirect_url;
                return;
            } else {
                throw new Error(data.detail || 'Sign up failed');
            }
        }

        // 2. Fallback for unexpected HTML response
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        window.location.reload();

    } catch (error) {
        console.error('Sign up error:', error);
        showNotification(error.message || 'Network error. Please check your connection.', 'danger');
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
}

/**
 * Initialize sign-up page functionality
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
    const signUpForm = document.querySelector('form');
    if (signUpForm) {
        signUpForm.addEventListener('submit', handleSignUpSubmit);
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
