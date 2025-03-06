from datetime import datetime
import sqlite3

class DatabaseManager:
    def __init__(self, db_path='user_progress.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            # Create progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS progress (
                    user_id TEXT,
                    module TEXT,
                    score REAL,
                    timestamp DATETIME,
                    FOREIGN KEY(user_id) REFERENCES users(username)
                )
            ''')
            conn.commit()

    def authenticate(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password))
            return cursor.fetchone() is not None

    def register_user(self, username, password):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                               (username, password))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def save_progress(self, username, module, score):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO progress (user_id, module, score, timestamp) 
                VALUES (?, ?, ?, ?)
            ''', (username, module, score, datetime.now()))
            conn.commit()

    def get_user_progress(self, username):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT module, MAX(score) as max_score, timestamp 
                FROM progress 
                WHERE user_id = ? 
                GROUP BY module
            ''', (username,))
            return {row[0]: {"max_score": row[1], "timestamp": row[2]} 
                    for row in cursor.fetchall()}
