// CoopConnect AI - API Integration

const API_BASE_URL = 'http://localhost:8000/api';

// Utility to get auth token
function getAuthToken() {
    return localStorage.getItem('coopconnect_token');
}

function setAuthToken(token) {
    localStorage.setItem('coopconnect_token', token);
}

// Global Fetch Wrapper with Auth Header
async function fetchAPI(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers
        });
        
        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || 'API request failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

// API Services
const API = {
    // Auth
    login: async (email, password) => {
        // FastAPI OAuth2 uses form data
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        if (!res.ok) throw new Error('Login failed');
        const data = await res.json();
        setAuthToken(data.access_token);
        return data;
    },
    
    register: async (userData) => {
        return await fetchAPI('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    },

    // Services
    getServices: async () => {
        return await fetchAPI('/services');
    },

    // Workers
    getWorkers: async () => {
        return await fetchAPI('/workers');
    },

    getWorker: async (id) => {
        return await fetchAPI(`/workers/${id}`);
    },

    // Bookings
    createBooking: async (bookingData) => {
        return await fetchAPI('/bookings', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    },

    getBookings: async () => {
        return await fetchAPI('/bookings');
    },

    updateBookingStatus: async (id, status) => {
        return await fetchAPI(`/bookings/${id}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status })
        });
    },

    // AI
    getAIMatch: async (matchData) => {
        return await fetchAPI('/ai/match', {
            method: 'POST',
            body: JSON.stringify(matchData)
        });
    },

    getAIForecast: async () => {
        return await fetchAPI('/ai/forecast');
    },

    // Admin
    getAdminDashboard: async () => {
        return await fetchAPI('/admin/dashboard');
    }
};

// Example usage to replace static DATA in UI
async function fetchAndRenderServices() {
    try {
        const services = await API.getServices();
        if (services && services.length > 0) {
            // Overwrite DATA object temporarily if using hybrid approach
            window.DATA = window.DATA || {};
            window.DATA.services = services;
            if (typeof renderServices === 'function') {
                renderServices();
            }
        }
    } catch (e) {
        console.log("Using static data fallback for services.");
    }
}

// Call on load if you want dynamic data replacement
// document.addEventListener('DOMContentLoaded', () => {
//     fetchAndRenderServices();
// });
