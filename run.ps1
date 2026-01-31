#!/usr/bin/env powershell
# ASQ Lists - Запуск сервера + туннель через localtunnel

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("local", "tunnel")]
    [string]$Mode = "local"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 ASQ LISTS - СЕРВЕР" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Проверить Python
Write-Host "📋 Проверка зависимостей..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python установлен" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не установлен!" -ForegroundColor Red
    exit 1
}

# Функция для запуска сервера
function Start-Server {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "🖥️  ЗАПУСКАЮ СЕРВЕР..." -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 URL: http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Аккаунт для тестирования:" -ForegroundColor Gray
    Write-Host "  Логин: kazah" -ForegroundColor White
    Write-Host "  Пароль: 88888888" -ForegroundColor White
    Write-Host ""
    Write-Host "Нажми Ctrl+C чтобы остановить" -ForegroundColor Gray
    Write-Host ""
    
    python debug_server.py
}

# Функция для запуска сервера + туннель
function Start-ServerWithTunnel {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "🖥️  ЗАПУСКАЮ СЕРВЕР..." -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Мониторь этот терминал для URL туннеля!" -ForegroundColor Yellow
    Write-Host ""
    
    # Запустить сервер в фоне
    $process = Start-Process python -ArgumentList "debug_server.py" -NoNewWindow -PassThru
    $pid = $process.Id
    
    Write-Host "✅ Сервер запущен (PID: $pid)" -ForegroundColor Green
    
    # Подождать пока сервер запустится
    Start-Sleep -Seconds 2
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "🌐 СОЗДАЮ ТУННЕЛЬ..." -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Запустить localtunnel
    lt --port 8000 --open
}

# Выбрать режим
if ($Mode -eq "tunnel") {
    Start-ServerWithTunnel
} else {
    Start-Server
}
