#!/usr/bin/env powershell
# ASQ Lists - Стартовый скрипт

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 ASQ LISTS - QUICK START" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверить Python
Write-Host "📋 Проверка Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не установлен!" -ForegroundColor Red
    exit 1
}

# Проверить Node.js
Write-Host "📋 Проверка Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Node.js не установлен (опционально для localtunnel)" -ForegroundColor Yellow
}

# Проверить localtunnel
Write-Host "📋 Проверка localtunnel..." -ForegroundColor Yellow
try {
    $ltVersion = lt --version
    Write-Host "✅ localtunnel: $ltVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️ localtunnel не установлен. Устанавливаю..." -ForegroundColor Yellow
    npm install -g localtunnel
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📁 ВАРИАНТЫ ЗАПУСКА:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  ЛОКАЛЬНЫЙ (http://localhost:8000):" -ForegroundColor Cyan
Write-Host "   python debug_server.py" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣  ЧЕРЕЗ ТУННЕЛЬ (интернет доступ):" -ForegroundColor Cyan
Write-Host "   1. Запустить сервер: python debug_server.py" -ForegroundColor White
Write-Host "   2. В новом терминале: lt --port 8000" -ForegroundColor White
Write-Host "   3. Скопировать URL из вывода" -ForegroundColor White
Write-Host "   4. Заменить API_URL в js/api.js" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎮 АККАУНТЫ ДЛЯ ТЕСТИРОВАНИЯ:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Логин:  kazah" -ForegroundColor White
Write-Host "Пароль: 88888888" -ForegroundColor White
Write-Host ""
Write-Host "Или создай новый аккаунт на странице логина" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✨ ВСЕ ФУНКЦИИ:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Список уровней с авторами и верификаторами" -ForegroundColor White
Write-Host "✅ Лидерборд с рейтингом игроков" -ForegroundColor White
Write-Host "✅ Аутентификация (login/register)" -ForegroundColor White
Write-Host "✅ Рулетка со случайными уровнями" -ForegroundColor White
Write-Host "✅ Тёмный режим" -ForegroundColor White
Write-Host "✅ Responsive дизайн" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🛠️ ЭНДПОИНТЫ API:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "POST /api/auth" -ForegroundColor Cyan
Write-Host "  • mode: 'login' или 'reg'" -ForegroundColor Gray
Write-Host "  • user: username" -ForegroundColor Gray
Write-Host "  • pwd: password" -ForegroundColor Gray
Write-Host ""
Write-Host "GET /api/leaderboard" -ForegroundColor Cyan
Write-Host "  • Получить лидерборд" -ForegroundColor Gray
Write-Host ""
Write-Host "POST /api/leaderboard" -ForegroundColor Cyan
Write-Host "  • action: 'get' или 'update'" -ForegroundColor Gray
Write-Host "  • user: username (для update)" -ForegroundColor Gray
Write-Host "  • score: число очков (для update)" -ForegroundColor Gray
Write-Host "  • level: имя уровня (для update)" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📂 ФАЙЛЫ ДАННЫХ:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "accounts.txt" -ForegroundColor Cyan
Write-Host "  • Хранилище аккаунтов (username:password)" -ForegroundColor Gray
Write-Host ""
Write-Host "leaderboard.json" -ForegroundColor Cyan
Write-Host "  • Данные лидерборда" -ForegroundColor Gray
Write-Host ""
Write-Host "data/*.json" -ForegroundColor Cyan
Write-Host "  • Уровни и конфигурация" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "⏹️  ОСТАНОВКА:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Нажми Ctrl+C в терминале для остановки" -ForegroundColor White
Write-Host ""

pause
