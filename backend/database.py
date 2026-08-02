import sqlite3
import os

# Gunakan /tmp di Vercel karena filesystemnya read-only
if os.environ.get('VERCEL') or os.environ.get('AWS_EXECUTION_ENV'):
    DB_PATH = '/tmp/chat.db'
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
