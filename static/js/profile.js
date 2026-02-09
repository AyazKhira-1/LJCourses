// ============================================
// PROFILE PAGE SPECIFIC JAVASCRIPT
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
 * Populate profile form with user data
 */
function populateProfile(userData) {
    // Header section
    document.getElementById('profile-name-header').textContent = userData.full_name || 'User';
    document.getElementById('profile-email-header').textContent = userData.email || '';

    // Profile photo
    const profilePhoto = document.getElementById('profile-photo');
    if (userData.profile_image) {
        profilePhoto.src = userData.profile_image;
    }

    // Form inputs
    document.getElementById('input-fullname').value = userData.full_name || '';
    document.getElementById('input-email').value = userData.email || '';
    document.getElementById('input-major').value = userData.major || '';
    document.getElementById('input-bio').value = userData.bio || '';

    // Store user ID for later use
    document.body.dataset.userId = userData.id;
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
            const profilePhoto = document.getElementById('profile-photo');
            const headerPhoto = document.getElementById('header-user-photo');

            if (data.photo_url) {
                profilePhoto.src = data.photo_url;
                if (headerPhoto) {
                    headerPhoto.src = data.photo_url;
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
 * Update profile data
 */
async function updateProfile(profileData) {
    const userId = document.body.dataset.userId;

    if (!userId) {
        showNotification('User ID not found', 'danger');
        return;
    }

    try {
        const response = await fetch(`/api/students/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(profileData)
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('Profile updated successfully!', 'success');

            // Update header with new name
            document.getElementById('profile-name-header').textContent = data.full_name || 'User';
            const headerName = document.getElementById('header-user-name');
            if (headerName) headerName.textContent = data.full_name;
        } else {
            showNotification(data.detail || 'Failed to update profile', 'danger');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showNotification('Network error. Please try again.', 'danger');
    }
}

/**
 * Initialize profile page
 */
document.addEventListener('DOMContentLoaded', async () => {
    // Fetch and populate user data - REMOVED: Managed by server-side rendering
    // const userData = await window.fetchUserProfile();
    // if (userData) {
    //     populateProfile(userData);
    // }

    // Photo upload button handler
    const photoButton = document.getElementById('photo-upload-btn');
    const fileInput = document.getElementById('photo-file-input');

    if (photoButton && fileInput) {
        photoButton.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                uploadProfilePhoto(file);
            }
        });
    }

    // Save changes button handler
    const saveButton = document.getElementById('save-profile-btn');
    if (saveButton) {
        saveButton.addEventListener('click', async (e) => {
            e.preventDefault();

            // Get form values
            const fullName = document.getElementById('input-fullname').value.trim();
            const major = document.getElementById('input-major').value.trim();
            const bio = document.getElementById('input-bio').value.trim();

            // Validate
            if (!fullName) {
                showNotification('Full name is required', 'danger');
                return;
            }

            // Prepare update data
            const updateData = {
                full_name: fullName,
                major: major || null,
                bio: bio || null
            };

            // Show loading state
            const originalText = saveButton.textContent;
            saveButton.disabled = true;
            saveButton.textContent = 'Saving...';

            // Update profile
            await updateProfile(updateData);

            // Restore button
            saveButton.disabled = false;
            saveButton.textContent = originalText;
        });
    }
});
