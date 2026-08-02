import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_URL = os.environ.get('POSTGRES_URL')

if POSTGRES_URL:
    # Use PostgreSQL on Vercel
    import psycopg2
    
    def get_connection():
        return psycopg2.connect(POSTGRES_URL)
        
    def init_db():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        
    def execute_query(cursor, query, params=()):
        query = query.replace('?', '%s')
        cursor.execute(query, params)

else:
    # Use SQLite locally
    import sqlite3
    
    DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')
    
    def get_connection():
        return sqlite3.connect(DB_PATH)
        
    def init_db():
        conn = get_connection()
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
        
    def execute_query(cursor, query, params=()):
        cursor.execute(query, params)

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
