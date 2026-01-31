// Frontend - GitHub Pages
export const SITE_URL = 'https://angyedz.github.io/ASQ-Lists';

// Backend для аккаунтов - через туннель localtunnel
// Замени это на URL из "lt --port 9000"
export const AUTH_URL = 'https://rohan-untarnishing-beula.ngrok-free.dev';

export const saveToken = (t) => localStorage.setItem('auth_token', t);
export const getToken = () => localStorage.getItem('auth_token');
export const clearToken = () => localStorage.removeItem('auth_token');

export async function apiCall(endpoint, options = {}) {
    try {
        // Определяем URL в зависимости от эндпоинта
        let baseUrl;
        if (endpoint.startsWith('/api/auth') || endpoint.startsWith('/api/leaderboard')) {
            // Аккаунты и лидерборд через туннель (backend)
            baseUrl = AUTH_URL;
        } else {
            // Остальное с фронтенда (локалхост)
            baseUrl = SITE_URL;
        }
        
        const headers = {
            'Content-Type': 'application/json',
            'X-User-Agent': 'ASQ-Lists-Client/1.0',
            'Referer': 'https://angyedz.github.io/'
        };
        
        // Добавляем Authorization только если есть токен и это защищённый эндпоинт
        const token = getToken();
        if (token && (endpoint.startsWith('/api/profile') || endpoint.startsWith('/api/leaderboard'))) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${baseUrl}${endpoint}`, {
            method: options.method || 'POST',
            headers: headers,
            body: options.body,
            credentials: 'omit'  // НЕ отправляем cookies/credentials
        });

        const result = await response.json();
        if (!response.ok) throw new Error(result.message || 'Ошибка сервера');
        return result;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}