from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, get_connection, execute_query
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Konfigurasi Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app)

# Initialize database when app starts
init_db()

@app.route('/api/messages', methods=['GET'])
def get_messages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role, content, timestamp FROM messages ORDER BY id ASC')
    messages = [{'role': row[0], 'content': row[1], 'timestamp': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(messages)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # Save user message
    execute_query(cursor, 'INSERT INTO messages (role, content) VALUES (?, ?)', ('user', user_message))
    
    # Simple rule-based response for Alda (since we don't have an AI API key yet)
    alda_response = generate_alda_response(user_message)
    
    # Save Alda's response
    execute_query(cursor, 'INSERT INTO messages (role, content) VALUES (?, ?)', ('assistant', alda_response))
    
    conn.commit()
    conn.close()
    
    return jsonify({'response': alda_response})

def generate_alda_response(message):
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Maaf, aku sedang mengalami kendala saat memproses permintaanmu. Coba lagi nanti ya!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
