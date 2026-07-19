# Quick Start Guide

This project consists of a Flask backend and a Vite+React frontend.

## How to Run

Instead of manually starting multiple terminals, you can use the helper script:

```bash
python run_project.py
```

### What this script does:
1.  **Checks for MongoDB**: Alerts you if MongoDB isn't running.
2.  **Manages Dependencies**: Automatically runs `npm install` if `node_modules` is missing.
3.  **Virtual Environment**: Automatically detects and uses the virtual environment in `server/venv`.
4.  **Concurrent Execution**: Starts both the Flask server and Vite development server in one terminal.
5.  **Graceful Shutdown**: Pressing `Ctrl+C` will stop both servers correctly.

## Prerequisites
- **Python 3.x**
- **Node.js & npm**
- **MongoDB** (Make sure it's running locally on port 27017)
