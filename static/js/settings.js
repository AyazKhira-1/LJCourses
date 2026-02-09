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
 * Populate settings form with user data
 */
function populateSettings(userData) {
    // Profile photo
    const profilePhoto = document.getElementById('settings-profile-photo');
    const photoUrl = userData.profile_image
        ? `http://127.0.0.1:8000${userData.profile_image}`
        : 'https://lh3.googleusercontent.com/aida-public/AB6AXuCGREimMqfkf59_cQFeFRyZhJ7dnNOxFTA76quRe9Xh7lFuFjiAb9zNThW98S85U3y0stXXHUu52pTnYyMNoMApThwBdAxf9wRz5uyhO267V6MGaILsWFT9eGc-xonTGNMZ9K9Mz5nGmKwI2MZYdXv4Erz4Lts0E0npK6ZC2GkM1gC1iUMiYqrMT_qzkeCwSsm32MYw49iQ_tP1bwxd7bOqcdIBikk0JdgON-eYHIVx6lI-2RtzoOsBDHOhSnvhmW2_bUpJF9SwZAo';

    if (profilePhoto) {
        profilePhoto.src = photoUrl;
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
        removePhotoBtn.style.display = userData.profile_image ? 'inline-block' : 'none';
    }
}

/**
 * Upload profile photo
 */
async function uploadProfilePhoto(file) {
    const token = window.getAuthToken();

    if (!token) {
        showNotification('Please login to upload photo', 'warning');
        return;
    }

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
        const response = await fetch('http://127.0.0.1:8000/api/upload/profile-photo', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Profile photo uploaded successfully!', 'success');

            // Update photo in UI
            const profilePhoto = document.getElementById('settings-profile-photo');
            const headerPhoto = document.getElementById('header-user-photo');
            if (profilePhoto && headerPhoto) {
                profilePhoto.src = `http://127.0.0.1:8000${data.photo_url}`;
                headerPhoto.src = `http://127.0.0.1:8000${data.photo_url}`;
            }

            // Update localStorage
            localStorage.setItem('user_profile_photo', `http://127.0.0.1:8000${data.photo_url}`);

            // Show remove button
            const removePhotoBtn = document.getElementById('remove-photo-btn');
            if (removePhotoBtn) {
                removePhotoBtn.style.display = 'inline-block';
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
    const token = window.getAuthToken();
    const userId = document.body.dataset.userId;

    if (!token || !userId) {
        showNotification('Please login to remove photo', 'warning');
        return;
    }

    if (!confirm('Are you sure you want to remove your profile photo?')) {
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/students/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ profile_image: null })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Profile photo removed successfully!', 'success');

            // Reset to default photo
            const defaultPhoto = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCGREimMqfkf59_cQFeFRyZhJ7dnNOxFTA76quRe9Xh7lFuFjiAb9zNThW98S85U3y0stXXHUu52pTnYyMNoMApThwBdAxf9wRz5uyhO267V6MGaILsWFT9eGc-xonTGNMZ9K9Mz5nGmKwI2MZYdXv4Erz4Lts0E0npK6ZC2GkM1gC1iUMiYqrMT_qzkeCwSsm32MYw49iQ_tP1bwxd7bOqcdIBikk0JdgON-eYHIVx6lI-2RtzoOsBDHOhSnvhmW2_bUpJF9SwZAo';

            const profilePhoto = document.getElementById('settings-profile-photo');
            const headerPhoto = document.getElementById('header-user-photo');

            if (profilePhoto && headerPhoto) {
                profilePhoto.src = defaultPhoto;
                headerPhoto.src = defaultPhoto;
            }

            // Update localStorage
            localStorage.setItem('user_profile_photo', defaultPhoto);

            // Hide remove button
            const removePhotoBtn = document.getElementById('remove-photo-btn');
            if (removePhotoBtn) {
                removePhotoBtn.style.display = 'none';
            }
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
    const token = window.getAuthToken();
    const userId = document.body.dataset.userId;

    if (!token || !userId) {
        showNotification('Please login to save settings', 'warning');
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
        const response = await fetch(`http://127.0.0.1:8000/api/students/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
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
    // Fetch and populate user data (using shared function from header.js)
    const userData = await window.fetchUserProfile();
    if (userData) {
        populateSettings(userData);
    }

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
