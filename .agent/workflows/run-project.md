---
description: Start the Serenity AI Project
---

### Prerequisites
- Python installed
- Node.js installed
- MongoDB running locally (default: port 27017)

### Steps to Run

#### 1. Start the Backend Server
```powershell
cd server
# If you haven't created the venv yet:
# python -m venv venv
# .\venv\Scripts\activate
# pip install -r requirements.txt
# python -m textblob.download_corpora lite

.\venv\Scripts\activate
python app.py
```

#### 2. Start the Frontend Client
Open a NEW terminal window:
```powershell
cd client
# If you haven't installed dependencies:
# npm install

npm run dev
```

#### 3. Access the Application
- Open your browser to [http://localhost:5173](http://localhost:5173)

### Troubleshooting
- **Frontend can't connect?** Ensure the backend is running on [http://localhost:5000](http://localhost:5000).
- **MongoDB Error?** Ensure MongoDB service is started on your machine.
