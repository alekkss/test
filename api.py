from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

JSON_FILE = '/var/www/novosty-top.ru/html/users.json'

# Получить всех пользователей
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Добавить нового пользователя
@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        # Читаем текущие данные
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Получаем данные нового пользователя
        new_user = request.json
        
        # Генерируем новый ID
        if data['users']:
            new_id = max(user['id'] for user in data['users']) + 1
        else:
            new_id = 1
        
        new_user['id'] = new_id
        
        # Добавляем пользователя
        data['users'].append(new_user)
        
        # Сохраняем в файл
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'user': new_user}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print('hello')
    app.run(host='0.0.0.0', port=5000)
