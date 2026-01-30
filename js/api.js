export const API_URL = window.location.origin;
const WORKER_URL = 'steep-sea-e479.hdigdi89.workers.dev';

export const saveToken = (t) => localStorage.setItem('auth_token', t);
export const getToken = () => localStorage.getItem('auth_token');
export const clearToken = () => localStorage.removeItem('auth_token');

export async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${WORKER_URL}${endpoint}`, {
            method: options.method || 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: options.body
        });

        const result = await response.json();
        if (!response.ok) throw new Error(result.message || 'Ошибка сервера');
        return result;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}