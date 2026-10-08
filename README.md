# 🧠 AI Mental Health Support Platform

An AI-powered mental health support platform that allows users to express their thoughts and feelings and communicate with an AI assistant without having to disclose their identity.

## ✨ Features

- 🔒 Anonymous user interaction
- 💬 AI-powered conversational support
- 🤖 LLM integration
- 🔐 User authentication
- 💾 Conversation management
- 🌐 Full-stack web application
- 📱 Responsive user interface

## 🛠️ Tech Stack

### Frontend
- React
- JavaScript

### Backend
- Python
- Flask

### Database
- MongoDB

### AI
- Large Language Model (LLM)

## 🏗️ Architecture

```text
                 User
                  │
                  ▼
          React Frontend
                  │
             HTTP / API
                  │
                  ▼
           Flask Backend
             │       │
             ▼       ▼
         MongoDB    LLM
             │       │
             └───┬───┘
                 ▼
          Backend Response
                 │
                 ▼
          React Frontend
                 │
                 ▼
              User
