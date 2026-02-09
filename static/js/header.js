// ============================================
// HEADER USER DATA & LOGOUT FUNCTIONALITY
// ============================================

/**
 * Get authentication token from localStorage
 */
function getAuthToken() {
    return localStorage.getItem('access_token');
}

/**
 * Fetch current user profile data from API
 */
async function fetchUserProfile() {
    const token = getAuthToken();

    if (!token) {
        console.warn('No auth token found');
        return null;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/auth/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            const userData = await response.json();
            return userData;
        } else if (response.status === 401) {
            console.warn('Session expired');
            localStorage.clear();
            window.location.href = '/student_login';
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

    if (headerUserPhoto) {
        const photoUrl = userData.profile_image
            ? `http://127.0.0.1:8000${userData.profile_image}`
            : 'https://lh3.googleusercontent.com/aida-public/AB6AXuCGREimMqfkf59_cQFeFRyZhJ7dnNOxFTA76quRe9Xh7lFuFjiAb9zNThW98S85U3y0stXXHUu52pTnYyMNoMApThwBdAxf9wRz5uyhO267V6MGaILsWFT9eGc-xonTGNMZ9K9Mz5nGmKwI2MZYdXv4Erz4Lts0E0npK6ZC2GkM1gC1iUMiYqrMT_qzkeCwSsm32MYw49iQ_tP1bwxd7bOqcdIBikk0JdgON-eYHIVx6lI-2RtzoOsBDHOhSnvhmW2_bUpJF9SwZAo';
        headerUserPhoto.src = photoUrl;
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

    try {
        // Get the access token from localStorage
        const token = localStorage.getItem('access_token');

        if (token) {
            // Call the FastAPI logout API to set is_active = False
            await fetch('http://127.0.0.1:8000/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.error('Logout API call failed:', error);
        // Continue with logout even if API call fails
    } finally {
        // Clear all localStorage data
        localStorage.clear();

        // Redirect to Flask logout to clear session
        window.location.href = '/logout';
    }
}

/**
 * Initialize header functionality
 */
document.addEventListener('DOMContentLoaded', () => {
    // Load header user data
    loadHeaderUserData();

    // Setup logout buttons
    const logoutButtons = document.querySelectorAll('[data-action="logout"]');
    logoutButtons.forEach(button => {
        button.addEventListener('click', handleLogout);
    });
});

// Expose functions globally for use in other scripts
window.fetchUserProfile = fetchUserProfile;
window.getAuthToken = getAuthToken;
