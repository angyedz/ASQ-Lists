import telebot
import jwt
import json
import secrets
import os
from datetime import datetime, timedelta
from shield import PasswordManager

# --- КОНФИГ ---
TOKEN = '8456640257:AAE_bwy6s3N604rnbpYbFqb153iM9cDE63I'
MY_ID = 1673415110
bot = telebot.TeleBot(TOKEN)
pm = PasswordManager('accounts.txt')
SECRET_KEY = "hell0h3ndsh3ke@#*(&@$KXSF9)" # Замени на свою строку
LEADERBOARD = []

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('user')
    except: return None

def process_logic(data):
    route = data.get('route')
    
    # AUTH
    if route == '/api/auth':
        user, pwd, mode = data.get('user', ''), data.get('pwd', ''), data.get('mode', '')
        if mode == 'login':
            if pm.check_user(user, pwd):
                token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm='HS256')
                return {'status': 'success', 'user': user, 'token': token}, 200
            return {'status': 'error', 'message': 'Invalid credentials'}, 401
        elif mode == 'reg':
            res = pm.register_user(user, pwd)
            if res['status'] == 'success':
                token = jwt.encode({'user': user, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm='HS256')
                return {'status': 'success', 'user': user, 'token': token}, 200
            return res, 400

    # PROFILE
    elif route == '/api/profile':
        user = verify_token(data.get('token', ''))
        if not user: return {'status': 'error', 'message': 'Unauthorized'}, 401
        entry = next((u for u in LEADERBOARD if u['user'] == user), None)
        return {'status': 'success', 'profile': {'user': user, 'rank': LEADERBOARD.index(entry)+1 if entry else 0, 'totalPoints': entry['score'] if entry else 0}}, 200

    # LEADERBOARD
    elif route == '/api/leaderboard':
        if data.get('method') == 'POST':
            user, score = data.get('user', ''), data.get('score', 0)
            entry = next((u for u in LEADERBOARD if u['user'] == user), None)
            if entry: entry['score'] = max(entry['score'], score)
            else: LEADERBOARD.append({'user': user, 'score': score})
            LEADERBOARD.sort(key=lambda x: x['score'], reverse=True)
        return {'status': 'success', 'leaderboard': LEADERBOARD}, 200

    # HEALTH & BATTERY (Твоя задача №4)
    elif route == '/api/health':
        try:
            with open("/sys/class/power_supply/battery/temp", "r") as f:
                temp = int(f.read()) / 10
        except: temp = "N/A"
        return {'status': 'healthy', 'battery_temp': temp, 'timestamp': datetime.now().isoformat()}, 200

    return {'status': 'error', 'message': 'Not Found'}, 404

@bot.message_handler(func=lambda m: m.chat.id == MY_ID)
def handle(m):
    try:
        req = json.loads(m.text)
        res, code = process_logic(req)
        bot.reply_to(m, json.dumps({"data": res, "code": code}))
    except: pass

if __name__ == '__main__':
    print("🚀 Backend is running...")
    bot.infinity_polling()