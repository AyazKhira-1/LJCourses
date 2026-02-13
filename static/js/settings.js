// ============================================
// SETTINGS PAGE SPECIFIC JAVASCRIPT
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
 * Select theme from settings card
 */
function selectTheme(theme) {
    // Call common function to set theme
    if (typeof setTheme === 'function') {
        setTheme(theme);
    } else {
        // Fallback if common.js hasn't loaded (unlikely)
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
    }

    updateThemeCards(theme);
}

/**
 * Update active state of theme cards
 */
function updateThemeCards(theme) {
    const lightCard = document.getElementById('lightThemeCard');
    const darkCard = document.getElementById('darkThemeCard');

    if (!lightCard || !darkCard) return;

    if (theme === 'dark') {
        lightCard.classList.remove('active');
        darkCard.classList.add('active');

        // Update icons
        lightCard.querySelector('.theme-check-icon')?.classList.replace('check_circle', 'radio_button_unchecked');
        lightCard.querySelector('.theme-check-icon')?.classList.replace('text-primary', 'text-secondary');

        darkCard.querySelector('.theme-uncheck-icon')?.classList.replace('radio_button_unchecked', 'check_circle');
        darkCard.querySelector('.theme-uncheck-icon')?.classList.replace('text-secondary', 'text-primary');
    } else {
        darkCard.classList.remove('active');
        lightCard.classList.add('active');

        // Update icons
        darkCard.querySelector('.theme-uncheck-icon')?.classList.replace('check_circle', 'radio_button_unchecked');
        darkCard.querySelector('.theme-uncheck-icon')?.classList.replace('text-primary', 'text-secondary');

        lightCard.querySelector('.theme-check-icon')?.classList.replace('radio_button_unchecked', 'check_circle');
        lightCard.querySelector('.theme-check-icon')?.classList.replace('text-secondary', 'text-primary');
    }
}


/**
 * Populate settings form with user data
 */
function populateSettings(userData) {
    // Profile photo
    const profilePhoto = document.getElementById('settings-profile-photo');

    if (profilePhoto && userData.profile_image) {
        profilePhoto.src = userData.profile_image;
    }

    // Bio textarea
    const bioTextarea = document.getElementById('settings-bio');
    if (bioTextarea) {
        bioTextarea.value = userData.bio || '';
    }

    // Store user ID for later use
    document.body.dataset.userId = userData.id;

    // Show/hide remove photo button based on whether user has custom photo
    const removePhotoBtn = document.getElementById('remove-photo-btn');
    if (removePhotoBtn) {
        // Simple check: if path contains 'uploads', it's custom.
        // Otherwise it's the default avatar.
        const isDefault = !userData.profile_image || userData.profile_image.includes('default-user.svg');
        removePhotoBtn.style.display = isDefault ? 'none' : 'inline-block';
    }
}

/**
 * Upload profile photo
 */
async function uploadProfilePhoto(file) {
    // Validate file
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showNotification('Invalid file type. Please upload jpg, png, or webp', 'danger');
        return;
    }

    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
        showNotification('File too large. Maximum size is 5MB', 'danger');
        return;
    }

    // Create FormData
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload/profile-photo', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Profile photo uploaded successfully!', 'success');

            // Update photo in UI
            const profilePhoto = document.getElementById('settings-profile-photo');
            const headerPhoto = document.getElementById('header-user-photo');

            if (data.photo_url) {
                if (profilePhoto) profilePhoto.src = data.photo_url;
                if (headerPhoto) headerPhoto.src = data.photo_url;

                // Show remove button
                const removePhotoBtn = document.getElementById('remove-photo-btn');
                if (removePhotoBtn) {
                    removePhotoBtn.style.display = 'inline-block';
                }
            }
        } else {
            showNotification(data.detail || 'Failed to upload photo', 'danger');
        }
    } catch (error) {
        console.error('Error uploading photo:', error);
        showNotification('Network error. Please try again.', 'danger');
    }
}

/**
 * Remove profile photo
 */
async function removeProfilePhoto() {
    const userId = document.body.dataset.userId;

    if (!userId) {
        showNotification('User ID not found', 'warning');
        return;
    }

    if (!confirm('Are you sure you want to remove your profile photo?')) {
        return;
    }

    try {
        const response = await fetch(`/api/students/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ profile_image: null })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Profile photo removed successfully!', 'success');

            // Reset to default photo (would be better if backend returned the default URL or we refresh)
            // For now, reload the page to get fresh state from server
            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } else {
            showNotification(data.detail || 'Failed to remove photo', 'danger');
        }
    } catch (error) {
        console.error('Error removing photo:', error);
        showNotification('Network error. Please try again.', 'danger');
    }
}

/**
 * Save settings changes
 */
async function saveSettings() {
    const userId = document.body.dataset.userId;

    if (!userId) {
        showNotification('User ID not found', 'warning');
        return;
    }

    // Get bio value
    const bioTextarea = document.getElementById('settings-bio');
    const bio = bioTextarea ? bioTextarea.value.trim() : '';

    // Prepare update data
    const updateData = {
        bio: bio || null
    };

    try {
        const response = await fetch(`/api/students/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Settings saved successfully!', 'success');
        } else {
            showNotification(data.detail || 'Failed to save settings', 'danger');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('Network error. Please try again.', 'danger');
    }
}

/**
 * Initialize settings page
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize theme state
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
    updateThemeCards(currentTheme);

    // Listen for theme changes from navbar
    document.addEventListener('themeChanged', (e) => {
        updateThemeCards(e.detail.theme);
    });

    // Photo upload camera button handler
    const cameraButton = document.getElementById('photo-camera-btn');
    const fileInput = document.getElementById('photo-file-input');

    if (cameraButton && fileInput) {
        cameraButton.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                uploadProfilePhoto(file);
            }
        });
    }

    // Change photo button handler
    const changePhotoBtn = document.getElementById('change-photo-btn');
    if (changePhotoBtn && fileInput) {
        changePhotoBtn.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // Remove photo button handler
    const removePhotoBtn = document.getElementById('remove-photo-btn');
    if (removePhotoBtn) {
        removePhotoBtn.addEventListener('click', removeProfilePhoto);
    }

    // Save changes button handler
    const saveButton = document.getElementById('save-settings-btn');
    if (saveButton) {
        saveButton.addEventListener('click', async (e) => {
            e.preventDefault();

            // Show loading state
            const originalText = saveButton.textContent;
            saveButton.disabled = true;
            saveButton.textContent = 'Saving...';

            await saveSettings();

            // Restore button
            saveButton.disabled = false;
            saveButton.textContent = originalText;
        });
    }
});
