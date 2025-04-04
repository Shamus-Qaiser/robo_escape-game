import sqlite3
import json
from datetime import datetime

class GameAI:
    def __init__(self):
        self.sessions = {}
        self.leaderboard = []
        
    def init_session(self):
        session_id = str(len(self.sessions) + 1)
        self.sessions[session_id] = {
            "level": 1,
            "score": 0,
            "ai_learning": {
                "moves_learned": 0,
                "patterns": []
            },
            "start_time": datetime.now()
        }
        
        # Save to database
        conn = sqlite3.connect('ai_demo.db')
        c = conn.cursor()
        c.execute("INSERT INTO game_sessions (session_id, score, level, ai_data) VALUES (?, ?, ?, ?)",
                  (session_id, 0, 1, json.dumps(self.sessions[session_id]['ai_learning'])))
        conn.commit()
        conn.close()
        
        return session_id
    
    def process_move(self, session_id, move):
        if session_id not in self.sessions:
            return {"error": "Invalid session ID"}
        
        # Update game state based on move
        self.sessions[session_id]['score'] += 10
        self.sessions[session_id]['ai_learning']['moves_learned'] += 1
        
        # Random level progression
        if self.sessions[session_id]['score'] % 50 == 0:
            self.sessions[session_id]['level'] += 1
            
        # Update database
        conn = sqlite3.connect('ai_demo.db')
        c = conn.cursor()
        c.execute("UPDATE game_sessions SET score=?, level=?, ai_data=? WHERE session_id=?",
                  (self.sessions[session_id]['score'], 
                   self.sessions[session_id]['level'],
                   json.dumps(self.sessions[session_id]['ai_learning']),
                   session_id))
        conn.commit()
        conn.close()
        
        return {
            "session_id": session_id,
            "score": self.sessions[session_id]['score'],
            "level": self.sessions[session_id]['level'],
            "moves_learned": self.sessions[session_id]['ai_learning']['moves_learned'],
            "message": f"AI learned from your {move} move"
        }
    
    def get_leaderboard(self):
        conn = sqlite3.connect('ai_demo.db')
        c = conn.cursor()
        c.execute("SELECT session_id, score, level FROM game_sessions ORDER BY score DESC LIMIT 10")
        leaderboard = [{"session_id": row[0], "score": row[1], "level": row[2]} for row in c.fetchall()]
        conn.close()
        return leaderboard