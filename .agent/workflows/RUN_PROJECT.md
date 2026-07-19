---
description: Steps to run the Mental Health Chatbot project locally.
---
# Running the Mental Health Chatbot Project

This guide provides step-by-step instructions to set up and run both the server (Flask) and client (Vite + React) components of the application.

## Prerequisites
Ensure the following are installed and running on your system:
- **Node.js** (v16+)
- **Python** (v3.9+)
- **MongoDB** (Ensure the MongoDB service is running locally on port 27017)

## 1. Server Setup

Navigate to the server directory and set up the Python environment.

### a. Navigate to the server folder
```bash
cd server
```

### b. Set up Virtual Environment (Recommended)
If you haven't already created a virtual environment:
```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```cmd
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### c. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```
*Note: If you encounter issues with sentiment analysis, you may need to download TextBlob corpora:*
```bash
python -m textblob.download_corpora
```

### d. Configure Environment Variables
Ensure a `.env` file exists in the `server` directory with the following keys:
```env
MONGO_URI=mongodb://localhost:27017/mental_health_bot
SECRET_KEY=your_secret_key_here
XAI_API_KEY=your_groq_api_key_here
```
*Note: The project uses `XAI_API_KEY` for the API key, but the code currently points to Groq's API endpoint (`https://api.groq.com/openai/v1`). Ensure you use a valid API key for the service you intend to use.*

### e. Run the Server
Start the Flask server:
```bash
python app.py
```
The server will start on `http://localhost:5000`.

## 2. Client Setup

Open a new terminal window and navigate to the client directory.

### a. Navigate to the client folder
```bash
cd client
```

### b. Install Dependencies
Install the required Node.js packages:
```bash
npm install
```

### c. Run the Development Server
Start the Vite development server:
```bash
npm run dev
```
The client will typically start on `http://localhost:5173`. Open this URL in your browser to use the application.

## Troubleshooting
- **MongoDB Connection Error**: Ensure MongoDB is running locally. You can use MongoDB Compass to verify the connection.
- **API Key Error**: Double-check your `XAI_API_KEY` in the `.env` file.
- **Port Conflicts**: Ensure ports `5000` (server) and `5173` (client) are free.
