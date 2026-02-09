// ============================================
// HEADER USER DATA & LOGOUT FUNCTIONALITY
// ============================================

/**
 * Fetch current user profile data from API
 */
async function fetchUserProfile() {
    try {
        const response = await fetch('/api/auth/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            return await response.json();
        } else if (response.status === 401) {
            console.warn('User not authenticated');
            // Do not redirect here, just return null so header shows default state or nothing
            return null;
        } else {
            console.error('Failed to load profile data');
            return null;
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
        return null;
    }
}

/**
 * Load and populate header user data
 */
async function loadHeaderUserData() {
    const userData = await fetchUserProfile();

    if (!userData) {
        return null;
    }

    // Update header user name and role
    const headerUserName = document.getElementById('header-user-name');
    const headerUserRole = document.getElementById('header-user-role');
    const headerUserPhoto = document.getElementById('header-user-photo');

    if (headerUserName) {
        headerUserName.textContent = userData.full_name || 'User';
    }

    if (headerUserRole) {
        headerUserRole.textContent = userData.role || 'Student';
    }

    if (headerUserPhoto && userData.profile_image) {
        headerUserPhoto.src = userData.profile_image;
    }

    return userData;
}

/**
 * Handle logout
 */
async function handleLogout(event) {
    if (event) {
        event.preventDefault();
    }

    // Redirect to Flask logout which handles session clearing
    window.location.href = '/logout';
}

/**
 * Initialize header functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load header user data - REMOVED: Managed by server-side rendering
    // loadHeaderUserData();

    // Setup logout buttons
    const logoutButtons = document.querySelectorAll('[data-action="logout"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', handleLogout);
    });
});

// Expose functions globally for use in other scripts
window.fetchUserProfile = fetchUserProfile;
