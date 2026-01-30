// Автоматически определяет корень сайта (для доступа к папке /data)
export const API_URL = window.location.origin;

// Твой рабочий URL воркера
const WORKER_URL = 'https://steep-sea-e479.hdigdi89.workers.dev/';

// Ключ бота (нужен только для чтения ответов через getUpdates)
// В идеале его тоже проксировать через воркер, но для теста оставим так
const BOT_TOKEN = 'ТВОЙ_ТЕЛЕГРАМ_ТОКЕН'; 

// ============ JWT MANAGEMENT ============
export const saveToken = (t) => localStorage.setItem('auth_token', t);
export const getToken = () => localStorage.getItem('auth_token');
export const clearToken = () => localStorage.removeItem('auth_token');
export const hasToken = () => !!getToken();

// ============ API CALLS ============
export async function apiCall(endpoint, options = {}) {
    const body = options.body ? JSON.parse(options.body) : {};
    
    // Формируем запрос для воркера -> телеграма -> телефона
    const requestData = {
        action: 'send', // Команда для воркера
        route: endpoint,
        method: options.method || 'POST',
        token: getToken(),
        ...body
    };

    try {
        const res = await fetch(WORKER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const sent = await res.json();
        if (!sent.ok) throw new Error("Ошибка отправки в Telegram");
        
        const msgId = sent.result.message_id;
        return await waitForResponse(msgId);
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    }
}

async function waitForResponse(msgId) {
    // 15 попыток по 1.5 секунды (около 22 секунд ожидания)
    for (let i = 0; i < 15; i++) {
        await new Promise(r => setTimeout(r, 1500));

        // Проверяем наличие ответа через воркер
        const res = await fetch(`${WORKER_URL}?action=check&msgId=${msgId}`);
        const result = await res.json();

        if (result.found) {
            // result.data — это JSON, который прислал Python из Termux
            if (result.data.code >= 400) throw new Error(result.data.data.message);
            return result.data.data;
        }
    }
    throw new Error('Телефон не ответил вовремя. Проверь Termux!');
}