// ============================================
// PASSWORD RESET PAGE JAVASCRIPT
// Used by change_password.html
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
 * Validate password strength
 * Requirements:
 * - At least 8 characters long
 * - Include uppercase and lowercase letters
 * - Include at least one number
 * - Include at least one special character
 */
function validatePasswordStrength(password) {
    const errors = [];

    if (password.length < 8) {
        errors.push('Password must be at least 8 characters long');
    }

    if (!/[A-Z]/.test(password)) {
        errors.push('Password must include at least one uppercase letter');
    }

    if (!/[a-z]/.test(password)) {
        errors.push('Password must include at least one lowercase letter');
    }

    if (!/[0-9]/.test(password)) {
        errors.push('Password must include at least one number');
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push('Password must include at least one special character');
    }

    return {
        valid: errors.length === 0,
        errors: errors
    };
}

/**
 * Handle password reset form submission
 */
async function handlePasswordResetSubmit(event) {
    event.preventDefault();

    // Get form values
    const email = document.getElementById('email').value.trim();
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    // Validate email
    const emailValidation = validateEmail(email);
    if (!emailValidation.valid) {
        showNotification(emailValidation.message, 'danger');
        return;
    }

    // Validate passwords match
    if (newPassword !== confirmPassword) {
        showNotification('Passwords do not match', 'danger');
        return;
    }

    // Validate password strength
    const passwordValidation = validatePasswordStrength(newPassword);
    if (!passwordValidation.valid) {
        showNotification(passwordValidation.errors[0], 'danger');
        return;
    }

    // Prepare data for API
    const resetData = {
        email: email,
        new_password: newPassword,
        confirm_password: confirmPassword
    };

    // Show loading state
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';

    try {
        // Send POST request to Flask
        const response = await fetch('/api/auth/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(resetData)
        });

        const data = await response.json();

        if (response.ok) {
            // Success!
            showNotification('Password reset successful! Redirecting to login...', 'success');

            // Determine if we're on the change password page (user is logged in)
            // If so, we might want to logout explicitly.
            const isChangePasswordPage = window.location.pathname.includes('change-password');
            if (isChangePasswordPage) {
                // Call logout endpoint to clear session
                await fetch('/logout');
                localStorage.clear(); // Clear all local storage
            }

            // Redirect to login after 1.5 seconds
            setTimeout(() => {
                window.location.href = '/student-login';
            }, 1500);
        } else {
            // Handle error response
            const errorMessage = data.detail || 'Password reset failed. Please try again.';
            showNotification(errorMessage, 'danger');

            // Re-enable button
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    } catch (error) {
        console.error('Password reset error:', error);
        showNotification('Network error. Please check your connection and try again.', 'danger');

        // Re-enable button
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
}

/**
 * Initialize password reset page functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    // Password visibility toggles
    const passwordToggles = document.querySelectorAll('.form-icon-right.clickable');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function () {
            try {
                const targetId = this.getAttribute('data-target');
                const input = document.getElementById(targetId);

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
    const resetForm = document.getElementById('password-reset-form');
    if (resetForm) {
        resetForm.addEventListener('submit', handlePasswordResetSubmit);
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

    // Real-time password strength feedback
    const newPasswordInput = document.getElementById('new-password');
    if (newPasswordInput) {
        newPasswordInput.addEventListener('blur', function () {
            const password = this.value;
            if (password) {
                const validation = validatePasswordStrength(password);
                if (!validation.valid) {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            }
        });

        newPasswordInput.addEventListener('focus', function () {
            this.classList.remove('is-invalid', 'is-valid');
        });
    }

    // Real-time password match feedback
    const confirmPasswordInput = document.getElementById('confirm-password');
    if (confirmPasswordInput && newPasswordInput) {
        confirmPasswordInput.addEventListener('blur', function () {
            const password = newPasswordInput.value;
            const confirmPassword = this.value;

            if (confirmPassword) {
                if (password !== confirmPassword) {
                    this.classList.add('is-invalid');
                    showNotification('Passwords do not match', 'warning');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            }
        });

        confirmPasswordInput.addEventListener('focus', function () {
            this.classList.remove('is-invalid', 'is-valid');
        });
    }
});
