@echo off
REM ASQ Lists - Стартовый скрипт для Windows
REM Запуск: start.bat

cd /d "%~dp0"

echo.
echo ========================================
echo ASQ LISTS - QUICK START
echo ========================================
echo.

REM Проверить Python
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ERROR: Python не установлен!
    pause
    exit /b 1
)

echo Выберите режим запуска:
echo.
echo 1 - Локальный (http://localhost:8000) - РЕКОМЕНДУЕТСЯ
echo 2 - Через туннель (доступ из интернета)
echo 3 - Показать справку
echo.

set /p choice="Введи номер (1-3): "

if "%choice%"=="1" (
    echo.
    echo ========================================
    echo Запускаю локальный сервер...
    echo ========================================
    echo.
    echo URL: http://localhost:8000
    echo Логин: kazah, Пароль: 88888888
    echo.
    echo Нажми Ctrl+C чтобы остановить
    echo.
    python debug_server.py
) else if "%choice%"=="2" (
    echo.
    echo ========================================
    echo Запускаю сервер + туннель...
    echo ========================================
    echo.
    echo Терминал 1 (сервер):
    echo %cd%
    start cmd /k "python debug_server.py"
    
    timeout /t 3 /nobreak
    
    echo.
    echo Терминал 2 (туннель):
    echo.
    start cmd /k "lt --port 8000"
) else if "%choice%"=="3" (
    type QUICKSTART.md
) else (
    echo Неверный выбор!
    timeout /t 2 /nobreak
)
