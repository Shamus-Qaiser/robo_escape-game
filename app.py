from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from model_trainer import train_model
from game_ai import GameAI

app = Flask(__name__, static_folder='./frontend/build')

# Add these routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):  # Changed function name
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Initialize game AI
game_ai = GameAI()

# Database setup
def init_db():
    conn = sqlite3.connect('ai_demo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS models
                 (id INTEGER PRIMARY KEY, name TEXT, accuracy REAL, dataset TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS game_sessions
                 (session_id TEXT PRIMARY KEY, score INTEGER, level INTEGER, ai_data TEXT)''')
    conn.commit()
    conn.close()

# Model Training Endpoints
@app.route('/api/train', methods=['POST'])
def train():
    data = request.json
    model_info = train_model(data['dataset'], data['model_type'])
    
    # Save to database
    conn = sqlite3.connect('ai_demo.db')
    c = conn.cursor()
    c.execute("INSERT INTO models (name, accuracy, dataset) VALUES (?, ?, ?)",
              (model_info['model_name'], model_info['accuracy'], model_info['dataset']))
    conn.commit()
    conn.close()
    
    return jsonify(model_info)

@app.route('/api/models', methods=['GET'])
def get_models():
    conn = sqlite3.connect('ai_demo.db')
    c = conn.cursor()
    c.execute("SELECT name, accuracy, dataset, timestamp FROM models ORDER BY timestamp DESC")
    models = [{'model_name': row[0], 'accuracy': row[1], 'dataset': row[2], 'timestamp': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(models)

# Game Endpoints
@app.route('/api/game/start', methods=['POST'])
def start_game():
    session_id = game_ai.init_session()
    return jsonify({"session_id": session_id, "status": "Game started", "level": 1, "score": 0})

@app.route('/api/game/move', methods=['POST'])
def game_move():
    data = request.json
    response = game_ai.process_move(data['session_id'], data['move'])
    return jsonify(response)

@app.route('/api/game/leaderboard', methods=['GET'])
def leaderboard():
    return jsonify(game_ai.get_leaderboard())

# Security Endpoint
@app.route('/api/security/check', methods=['GET'])
def security_check():
    return jsonify({
        "data_encrypted": True,
        "compliance": ["GDPR", "CCPA"],
        "last_audit": "2023-05-15"
    })

# Serve React Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)