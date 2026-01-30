#!/usr/bin/env python3
"""
🖥️  ASQ List - Локальный хост для дебугинга
Всё работает на одном сервере - без CORS проблем

Запуск:
  python debug_server.py

Затем откройте: http://localhost:8000
"""

import http.server
import socketserver
import os
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8000

# Простое хранилище пользователей (в файле)
USERS_FILE = "accounts.txt"
LEADERBOARD_FILE = "leaderboard.json"


def load_users():
    """Загрузить пользователей из файла"""
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    username, password = line.split(':', 1)
                    users[username] = password
    return users


def save_users(users):
    """Сохранить пользователей в файл"""
    with open(USERS_FILE, 'w') as f:
        for username, password in users.items():
            f.write(f"{username}:{password}\n")


def load_leaderboard():
    """Загрузить лидерборд"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []


def save_leaderboard(data):
    """Сохранить лидерборд"""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(data, f, indent=2)


class DebugHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP обработчик для локального дебугинга"""
    
    def do_GET(self):
        """Обработка GET запросов"""
        # Serve static files
        if self.path == '/':
            self.path = '/index.html'
        
        # Serve API data
        if self.path.startswith('/api/data/'):
            self.handle_data_request()
            return
        
        # Serve API endpoints
        if self.path == '/api/profile':
            self.handle_get_profile()
            return
        
        if self.path == '/api/leaderboard':
            self.handle_get_leaderboard()
            return
        
        return super().do_GET()
    
    def handle_data_request(self):
        """Обработка запросов данных (JSON файлы)"""
        # Extract filename from path
        path = self.path.replace('/api/data/', '')
        
        # Remove query params
        if '?' in path:
            path = path.split('?')[0]
        
        # Safety: prevent directory traversal
        if '..' in path or path.startswith('/'):
            self.send_error(403, 'Forbidden')
            return
        
        # Construct file path
        file_path = os.path.join('data', path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"✗ Not found: {file_path}")
            self.send_error(404, f'File not found: {file_path}')
            return
        
        # Check if it's a JSON file
        if not file_path.endswith('.json'):
            self.send_error(403, 'Only JSON files allowed')
            return
        
        # Read and serve file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            
            self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
            print(f"✓ Served: {file_path}")
        except Exception as e:
            print(f"✗ Error serving {file_path}: {e}")
            self.send_error(500, f'Error reading file: {str(e)}')
    
    def do_POST(self):
        """Обработка POST запросов"""
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Get content length
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length == 0:
            self.send_error(400, 'No content')
            return
        
        # Read body
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
        except Exception as e:
            self.send_error(400, f'Invalid JSON: {str(e)}')
            return
        
        # Route endpoints
        if path == '/api/auth':
            self.handle_auth(data)
        elif path == '/api/leaderboard':
            self.handle_leaderboard(data)
        elif path == '/api/logout':
            self.handle_logout()
        else:
            self.send_error(404, 'Not Found')
    
    def handle_auth(self, data):
        """Обработка входа/регистрации"""
        username = data.get('user', '').strip()
        password = data.get('pwd', '').strip()
        mode = data.get('mode', '').strip()
        
        # Валидация
        if not username or not password:
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Username and password required'
            })
            return
        
        if len(username) < 3 or len(username) > 20:
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Username must be 3-20 characters'
            })
            return
        
        if len(password) < 8:
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Password must be at least 8 characters'
            })
            return
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Username can only contain letters, numbers, and underscores'
            })
            return
        
        users = load_users()
        
        if mode == 'login':
            if username in users and users[username] == password:
                print(f"✓ {username} logged in")
                self.send_json_response(200, {
                    'status': 'success',
                    'user': username
                })
            else:
                print(f"✗ {username} - invalid credentials")
                self.send_json_response(401, {
                    'status': 'error',
                    'message': 'Invalid credentials'
                })
        
        elif mode == 'reg':
            if username in users:
                print(f"✗ {username} - already exists")
                self.send_json_response(400, {
                    'status': 'error',
                    'message': 'User already exists'
                })
            else:
                users[username] = password
                save_users(users)
                print(f"✓ {username} registered")
                self.send_json_response(200, {
                    'status': 'success',
                    'user': username
                })
        
        else:
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Invalid mode (login or reg)'
            })
    
    def handle_leaderboard(self, data):
        """Обработка лидерборда"""
        action = data.get('action', '').strip()
        
        leaderboard = load_leaderboard()
        
        if action == 'get':
            self.send_json_response(200, {
                'status': 'success',
                'leaderboard': leaderboard
            })
        
        elif action == 'update':
            username = data.get('user', '').strip()
            score = int(data.get('score', 0))
            level = data.get('level', '').strip()
            
            if not username or not level:
                self.send_json_response(400, {
                    'status': 'error',
                    'message': 'Username and level required'
                })
                return
            
            # Find or create entry
            entry = next((e for e in leaderboard if e['user'] == username and e['level'] == level), None)
            
            if entry:
                entry['score'] = max(entry['score'], score)
            else:
                leaderboard.append({
                    'user': username,
                    'level': level,
                    'score': score
                })
            
            # Sort
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            
            save_leaderboard(leaderboard)
            print(f"✓ {username} - {level}: {score} points")
            
            self.send_json_response(200, {
                'status': 'success',
                'leaderboard': leaderboard
            })
        
        else:
            self.send_json_response(400, {
                'status': 'error',
                'message': 'Invalid action (get or update)'
            })
    
    def handle_get_profile(self):
        """Получить профиль текущего пользователя"""
        # Для дебугинга - просто возвращаем пустой профиль
        # В production нужна система сессий/токенов
        self.send_json_response(200, {
            'status': 'success',
            'profile': {
                'rank': 0,
                'totalPoints': 0,
                'completedLevels': []
            }
        })
    
    def handle_get_leaderboard(self):
        """Получить лидерборд через GET"""
        leaderboard = load_leaderboard()
        self.send_json_response(200, {
            'status': 'success',
            'leaderboard': leaderboard
        })
    
    def handle_logout(self):
        """POST /api/logout - Logout user"""
        self.send_json_response(200, {
            'status': 'success',
            'message': 'Logged out successfully'
        })
    
    def send_json_response(self, status_code, data):
        """Отправить JSON ответ"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store, no-cache')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def end_headers(self):
        """Добавить cache control headers"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Логирование"""
        # Skip logging errors for non-existent files (browser requests like .well-known)
        if args and len(args) > 0:
            # Convert args to string for checking
            args_str = str(args[0]) if args else ''
            if '/css/' not in args_str and '/js/' not in args_str and '/assets/' not in args_str and '.well-known' not in args_str:
                print(f"[{self.client_address[0]}] {format % args}")
        else:
            print(f"[{self.client_address[0]}] {format % args}")


def main():
    """Запустить сервер"""
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    print("=" * 70)
    print("🖥️  ASQ LIST - DEBUG SERVER")
    print("=" * 70)
    print()
    print(f"✅ Сервер на http://localhost:{PORT}")
    print(f"📁 Файлы из: {os.getcwd()}")
    print()
    print("📊 Данные пользователей:")
    print(f"  • accounts.txt (пользователи)")
    print(f"  • leaderboard.json (лидерборд)")
    print()
    print("🔧 Эндпоинты:")
    print("  • POST /api/auth (login, reg)")
    print("  • POST /api/leaderboard (get, update)")
    print()
    print("⌨️  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    with socketserver.TCPServer(("", PORT), DebugHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped.")


if __name__ == '__main__':
    main()
