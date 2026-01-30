import json
import jwt
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from shield import PasswordManager

app = Flask(__name__)
CORS(app)

# --- НАСТРОЙКИ ---
SECRET_KEY = "super_secret_key_123"
ACCOUNTS_FILE = 'accounts.txt'
LEADER_FILE = 'leaderboard.json'

pm = PasswordManager(ACCOUNTS_FILE)

def load_leaderboard():
    if os.path.exists(LEADER_FILE):
        with open(LEADER_FILE, 'r') as f: return json.load(f)
    return []

def save_leaderboard(data):
    with open(LEADER_FILE, 'w') as f: json.dump(data, f)

# --- РОУТЫ ---

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.json
    user, pwd, mode = data.get('user'), data.get('pwd'), data.get('mode')
    
    if mode == 'login':
        if pm.check_user(user, pwd):
            token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY)
            return jsonify({'status': 'success', 'token': token, 'user': user})
        return jsonify({'status': 'error', 'message': 'Неверный логин или пароль'}), 401
    
    elif mode == 'reg':
        res = pm.register_user(user, pwd)
        return jsonify(res), (200 if res['status'] == 'success' else 400)

@app.route('/api/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    scores = load_leaderboard()
    if request.method == 'POST':
        data = request.json
        user, score = data.get('user'), data.get('score', 0)
        
        entry = next((item for item in scores if item["user"] == user), None)
        if entry: entry['score'] = max(entry['score'], score)
        else: scores.append({"user": user, "score": score})
        
        scores.sort(key=lambda x: x['score'], reverse=True)
        save_leaderboard(scores)
        return jsonify({"status": "success", "leaderboard": scores})
    
    return jsonify({"status": "success", "leaderboard": scores})

@app.route('/api/health', methods=['GET'])
def health():
    try:
        with open("/sys/class/power_supply/battery/temp", "r") as f:
            temp = int(f.read()) / 10
    except: temp = "N/A"
    return jsonify({'status': 'online', 'battery_temp': temp})

if __name__ == '__main__':
    print("🚀 СЕРВЕР ЗАПУЩЕН НА ПОРТУ 8000")
    app.run(host='0.0.0.0', port=8000)