# Serenity AI – Mental Health Support Platform

Serenity AI is a full-stack AI-powered mental health support platform that provides users with a private space to express their thoughts, interact with an AI companion, and join anonymous topic-based support rooms.

## Features

- AI-powered mental health conversational support
- Emotion detection using TextBlob and keyword analysis
- Crisis keyword detection and safety response
- Anonymous real-time support rooms
- Automatically generated anonymous usernames
- MongoDB-based conversation history
- Automatic deletion of chat logs after 24 hours
- Real-time communication using Socket.IO
- Local knowledge-based fallback when the LLM is unavailable

## Tech Stack

**Frontend**
- React
- JavaScript
- React Router
- Tailwind CSS
- Socket.IO Client

**Backend**
- Python
- Flask
- Flask-SocketIO
- MongoDB
- PyMongo

**AI**
- Llama 3.3 70B via Groq
- TextBlob
- Prompt Engineering

## 🏗️ Architecture

```text
User
  ↓
React Frontend
  ↓
Flask / Socket.IO
  ↓
Emotion Detection
  ↓
Hybrid Chatbot
  ├── Llama 3.3 70B (Groq)
  └── Local Knowledge Base
  ↓
MongoDB
  ↓
Response to User
```

Support Rooms
Users can join different anonymous support rooms:
- Anxiety Support
- Depression Support
- Stress Relief
- Safe Space
The current prototype uses simulated anonymous peer users to create an active support-room experience.

Privacy
- Anonymous usernames for peer interactions
- Conversation data stored temporarily in MongoDB
- Chat logs automatically expire after 24 hours
- No requirement to provide a real name for peer-room interaction

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd Mental-Health-Support-Chatbot-Anonymous-Chatroom
```

### 2. Start the backend

```bash
cd server
pip install -r requirements.txt
python app.py
```

### 3. Start the frontend

```bash
cd client
npm install
npm run dev
```

