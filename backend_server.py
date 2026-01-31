#!/usr/bin/env python3
"""
🔐 ASQ Lists - Backend for Authentication & Leaderboard
Runs on localtunnel for secure auth

This server handles:
- User authentication (login/register)
- Leaderboard management
- User data storage

Frontend (http://localhost:8000) will connect to this via tunnel
"""

import http.server
import socketserver
import os
import json
import jwt
from datetime import datetime, timedelta
from urllib.parse import urlparse
import hashlib

PORT = 9000  # Different port for auth backend

# Configuration
SECRET_KEY = "your-secret-key-change-this"
ACCOUNTS_FILE = 'accounts.txt'
LEADERBOARD_FILE = 'leaderboard.json'

def hash_password(pwd):
    """Simple password hashing"""
    return hashlib.sha256(pwd.encode()).hexdigest()

def load_accounts():
    """Load user accounts from file"""
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        try:
            with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ':' in line:
                        user, pwd = line.split(':', 1)
                        accounts[user] = pwd
        except:
            pass
    return accounts

def save_accounts(accounts):
    """Save user accounts to file"""
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        for user, pwd in accounts.items():
            f.write(f"{user}:{pwd}\n")

def load_leaderboard():
    """Load leaderboard"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(data):
    """Save leaderboard"""
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    """Handle authentication requests"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        # Parse request
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length == 0:
            self.send_error(400, 'No content')
            return
        
        try:
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
        except:
            self.send_error(400, 'Invalid JSON')
            return
        
        # Route requests
        if path == '/api/auth':
            self.handle_auth(data)
        elif path == '/api/leaderboard':
            self.handle_leaderboard(data)
        else:
            self.send_error(404)
    
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == '/api/leaderboard':
            self.handle_get_leaderboard()
        elif path == '/health':
            self.send_json(200, {'status': 'ok'})
        else:
            self.send_error(404)
    
    def handle_auth(self, data):
        """Handle login/register"""
        user = data.get('user', '').strip()
        pwd = data.get('pwd', '').strip()
        mode = data.get('mode', '').strip()
        
        # Validate
        if not user or not pwd:
            self.send_json(400, {'status': 'error', 'message': 'Username and password required'})
            return
        
        if len(user) < 3 or len(user) > 20:
            self.send_json(400, {'status': 'error', 'message': 'Username must be 3-20 characters'})
            return
        
        if len(pwd) < 8:
            self.send_json(400, {'status': 'error', 'message': 'Password must be at least 8 characters'})
            return
        
        accounts = load_accounts()
        pwd_hash = hash_password(pwd)
        
        if mode == 'login':
            if user in accounts and accounts[user] == pwd_hash:
                # Create JWT token
                token = jwt.encode({
                    'user': user,
                    'exp': datetime.utcnow() + timedelta(days=7)
                }, SECRET_KEY, algorithm='HS256')
                
                self.send_json(200, {
                    'status': 'success',
                    'token': token,
                    'user': user
                })
                print(f"✓ {user} logged in")
            else:
                self.send_json(401, {'status': 'error', 'message': 'Invalid credentials'})
                print(f"✗ {user} - invalid credentials")
        
        elif mode == 'reg':
            if user in accounts:
                self.send_json(400, {'status': 'error', 'message': 'User already exists'})
                print(f"✗ {user} - already exists")
            else:
                accounts[user] = pwd_hash
                save_accounts(accounts)
                
                token = jwt.encode({
                    'user': user,
                    'exp': datetime.utcnow() + timedelta(days=7)
                }, SECRET_KEY, algorithm='HS256')
                
                self.send_json(200, {
                    'status': 'success',
                    'token': token,
                    'user': user
                })
                print(f"✓ {user} registered")
        else:
            self.send_json(400, {'status': 'error', 'message': 'Invalid mode'})
    
    def handle_leaderboard(self, data):
        """Handle leaderboard update"""
        action = data.get('action', '').strip()
        
        if action == 'update':
            user = data.get('user', '').strip()
            score = int(data.get('score', 0))
            level = data.get('level', '').strip()
            
            if not user or not level:
                self.send_json(400, {'status': 'error', 'message': 'User and level required'})
                return
            
            leaderboard = load_leaderboard()
            
            # Find or create entry
            entry = next((e for e in leaderboard if e['user'] == user and e['level'] == level), None)
            if entry:
                entry['score'] = max(entry['score'], score)
            else:
                leaderboard.append({'user': user, 'level': level, 'score': score})
            
            # Sort
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            save_leaderboard(leaderboard)
            
            self.send_json(200, {'status': 'success', 'leaderboard': leaderboard})
            print(f"✓ {user} - {level}: {score}")
        else:
            self.send_json(400, {'status': 'error', 'message': 'Invalid action'})
    
    def handle_get_leaderboard(self):
        """Get leaderboard"""
        leaderboard = load_leaderboard()
        self.send_json(200, {'status': 'success', 'leaderboard': leaderboard})
    
    def send_json(self, status, data):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[AUTH] {format % args}")

def main():
    os.chdir(os.path.dirname(__file__))
    
    print("=" * 70)
    print("🔐 ASQ LIST - AUTHENTICATION SERVER")
    print("=" * 70)
    print()
    print(f"📍 Backend на http://localhost:{PORT}")
    print(f"🌐 Используй с туннелем: lt --port {PORT}")
    print()
    print("📚 Эндпоинты:")
    print("  • POST /api/auth (mode: login или reg)")
    print("  • GET /api/leaderboard")
    print("  • POST /api/leaderboard (action: update)")
    print()
    print("⌨️  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    with socketserver.TCPServer(("", PORT), AuthHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped.")

if __name__ == '__main__':
    main()
