const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');
const API_URL = 'http://localhost:5000/api/chat';

// Fetch history on load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('http://localhost:5000/api/messages');
        if (response.ok) {
            const messages = await response.json();
            // Clear default welcome if there is history
            if (messages.length > 0) {
                chatBox.innerHTML = ''; 
                messages.forEach(msg => {
                    appendMessage(msg.role === 'user' ? 'user' : 'alda', msg.content);
                });
            }
        }
    } catch (error) {
        console.error('Error fetching history:', error);
    }
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // 1. Add user message to UI
    appendMessage('user', message);
    userInput.value = '';
    
    // 2. Show typing indicator
    const typingId = showTypingIndicator();
    
    // 3. Send to backend
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        // 4. Remove typing indicator and show response
        removeTypingIndicator(typingId);
        
        if (data.response) {
            appendMessage('alda', data.response);
        } else {
            appendMessage('alda', 'Maaf, terjadi kesalahan saat memproses pesan.');
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingId);
        appendMessage('alda', 'Maaf, aku tidak bisa terhubung ke server saat ini. Pastikan backend sudah berjalan.');
    }
});

function appendMessage(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'alda-message');
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('msg-content');
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    
    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'alda-message');
    typingDiv.id = id;
    
    const indicatorDiv = document.createElement('div');
    indicatorDiv.classList.add('typing-indicator');
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('typing-dot');
        indicatorDiv.appendChild(dot);
    }
    
    typingDiv.appendChild(indicatorDiv);
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    
    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}
