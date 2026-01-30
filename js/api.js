const WORKER_URL = 'https://steep-sea-e479.hdigdi89.workers.dev/';

export const saveToken = (t) => localStorage.setItem('auth_token', t);
export const getToken = () => localStorage.getItem('auth_token');
export const clearToken = () => localStorage.removeItem('auth_token');

export async function apiCall(endpoint, options = {}) {
    const body = options.body ? JSON.parse(options.body) : {};
    
    // 1. Отправляем запрос через воркер
    const res = await fetch(WORKER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'send',
            route: endpoint,
            method: options.method || 'POST',
            token: getToken(),
            ...body
        })
    });

    const sent = await res.json();
    const msgId = sent.result.message_id;

    // 2. Ждем ответ (тоже через воркер)
    return await waitForResponse(msgId);
}

async function waitForResponse(msgId) {
    for (let i = 0; i < 15; i++) {
        await new Promise(r => setTimeout(r, 1500)); // Ждем 1.5 сек

        // Просим воркер проверить, не ответил ли телефон
        const res = await fetch(`${WORKER_URL}?action=check&msgId=${msgId}`);
        const result = await res.json();

        if (result.found) {
            if (result.data.code >= 400) throw new Error(result.data.data.message);
            return result.data.data;
        }
    }
    throw new Error('Телефон не в сети. Проверь Termux!');
}