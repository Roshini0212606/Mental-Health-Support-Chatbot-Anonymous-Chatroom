import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Database Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/mental_health_bot')
try:
    client = MongoClient(MONGO_URI)
    db = client.get_database()
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

# Initialize Chatbot & Events
from chatbot import HybridChatbot
from socket_events import register_socket_events

@app.route('/api/history/<room_id>', methods=['GET'])
def get_chat_history(room_id):
    history = chatbot.chat_log_model.get_recent_history(room_id, limit=20)
    # Convert to the format the frontend expects
    frontend_history = []
    for msg in history:
        frontend_history.append({
            "text": msg["content"],
            "sender": "bot" if msg["role"] == "assistant" else "user",
            "emotion": "Neutral" # We could store/retrieve this too if needed
        })
    return jsonify(frontend_history)

chatbot = HybridChatbot(db)
register_socket_events(socketio, chatbot)


@app.route('/')
def home():
    return jsonify({"message": "Mental Health Chatbot API is running"})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_message = data.get('message')
    room_id = data.get('room_id', 'default_api_room')
    user_id = data.get('user_id', 'anonymous_api_user')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # 1. Fetch history
    history = chatbot.chat_log_model.get_recent_history(room_id)
    
    # 2. Get AI Response
    response = chatbot.get_response(user_message, history=history)
    
    # 3. Log user message
    chatbot.chat_log_model.log_message(
        room_id=room_id,
        user_id=user_id,
        message=user_message,
        role='user',
        emotion=response['detected_emotion']
    )
    
    # 4. Log AI response
    chatbot.chat_log_model.log_message(
        room_id=room_id,
        user_id="Serenity",
        message=response['response'],
        role='assistant',
        emotion=response['detected_emotion']
    )

    return jsonify({
        "response": response['response'],
        "detected_emotion": response['detected_emotion'],
        "source": response.get('source'),
        "room_id": room_id
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
