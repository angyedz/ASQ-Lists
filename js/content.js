import { round, score } from './score.js';
import { AUTH_URL, apiCall } from './api.js';

/**
 * Путь к папке с JSON данными уровней (статике)
 * GitHub Pages URL с полным путём включая /ASQ-Lists/
 */
const dir = 'https://angyedz.github.io/ASQ-Lists/data';

export async function fetchList() {
    try {
        const listResult = await fetch(`${dir}/_list.json`);
        if (!listResult.ok) throw new Error("Не удалось загрузить _list.json");
        
        const list = await listResult.json();
        return await Promise.all(
            list.map(async (path, rank) => {
                try {
                    const levelResult = await fetch(`${dir}/${path}.json`);
                    const level = await levelResult.json();
                    return [
                        {
                            ...level,
                            path,
                            records: level.records.sort((a, b) => b.percent - a.percent),
                        },
                        null,
                    ];
                } catch {
                    console.error(`Ошибка загрузки уровня #${rank + 1}: ${path}`);
                    return [null, path];
                }
            })
        );
    } catch (e) {
        console.error("Ошибка загрузки списка уровней:", e);
        return []; // Возвращаем пустой массив, чтобы сайт не "умер"
    }
}

export async function fetchEditors() {
    try {
        const res = await fetch(`${dir}/_editors.json`);
        return await res.json();
    } catch {
        return null;
    }
}

/**
 * Получаем лидерборд напрямую с твоего Android!
 */
export async function fetchLeaderboard() {
    try {
        // Запрос идет через Cloudflare Worker прямо в Flask на телефоне
        const data = await apiCall('/api/leaderboard', { method: 'GET' });
        
        if (data && data.leaderboard) {
            // Возвращаем отсортированные данные с телефона
            return [data.leaderboard, []];
        }
    } catch (e) {
        console.error("Не удалось получить лидерборд с сервера:", e);
    }

    // Если сервер на телефоне оффлайн, можно вернуть пустой список или статику
    return [[], ["Сервер Android оффлайн"]];
}