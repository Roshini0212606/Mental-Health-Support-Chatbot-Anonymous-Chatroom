import subprocess
import sys
import os
import time
import signal
import socket

# Configuration
SERVER_DIR = "server"
CLIENT_DIR = "client"
FLASK_PORT = 5000
VITE_PORT = 5173

def print_status(message, type="info"):
    colors = {
        "info": "\033[94m",    # Blue
        "success": "\033[92m", # Green
        "warning": "\033[93m", # Yellow
        "error": "\033[91m",   # Red
        "reset": "\033[0m"     # Reset
    }
    # Check if stdout supports colors (mostly true for modern terminals)
    if os.name == 'nt' and not os.environ.get('WT_SESSION'):
        # Just simple print for old Windows CMD
        print(f"[{type.upper()}] {message}")
    else:
        print(f"{colors.get(type, colors['info'])}[{type.upper()}] {message}{colors['reset']}")

def run_command(command, cwd=None, env=None, shell=False):
    """Run a command and print output on failure."""
    try:
        subprocess.check_call(command, cwd=cwd, env=env, shell=shell)
    except subprocess.CalledProcessError:
        print_status(f"Failed to run: {' '.join(command) if isinstance(command, list) else command}", "error")
        sys.exit(1)

def check_mongodb():
    """Check if MongoDB is running on the default port."""
    print_status("Checking MongoDB...", "info")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(('localhost', 27017))
        print_status("MongoDB is running.", "success")
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError):
        print_status("MongoDB does not seem to be running on localhost:27017.", "warning")
        print_status("Please ensure MongoDB is started if your app requires it.", "warning")
        return False

def get_python_executable():
    """Return path to python in venv if it exists, otherwise use current interpreter."""
    venv_path = os.path.join(SERVER_DIR, "venv")
    if os.name == 'nt':
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_exe = os.path.join(venv_path, "bin", "python")
    
    if os.path.exists(python_exe):
        print_status(f"Using virtual environment: {venv_path}", "info")
        return python_exe
    
    print_status("Virtual environment not found, using system Python.", "warning")
    return sys.executable

def install_dependencies(python_exe):
    """Install Python and Node.js dependencies."""
    print_status("--- Phase 1: Installing Dependencies ---", "info")
    
    # Python
    req_file = os.path.join(SERVER_DIR, "requirements.txt")
    if os.path.exists(req_file):
        print_status("Installing Python dependencies...", "info")
        run_command([python_exe, "-m", "pip", "install", "-r", "requirements.txt"], cwd=SERVER_DIR)
    
    # Node.js
    if os.path.exists(os.path.join(CLIENT_DIR, "package.json")):
        print_status("Installing Node.js dependencies...", "info")
        run_command(["npm", "install"], cwd=CLIENT_DIR, shell=True)

def start_processes(python_exe):
    """Start Flask and Vite servers."""
    print_status("--- Phase 2: Starting Servers ---", "info")
    
    processes = []
    
    # 1. Start Flask Server
    print_status(f"Starting Backend on port {FLASK_PORT}...", "info")
    server_env = os.environ.copy()
    server_env["PYTHONUNBUFFERED"] = "1"
    
    server_proc = subprocess.Popen(
        [python_exe, "app.py"],
        cwd=SERVER_DIR,
        env=server_env
    )
    processes.append(("Backend", server_proc))

    # 2. Start Vite Client
    print_status(f"Starting Frontend (Vite)...", "info")
    client_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=CLIENT_DIR,
        shell=True
    )
    processes.append(("Frontend", client_proc))

    print_status("\nProject is launching!", "success")
    print_status(f"Backend:  http://localhost:{FLASK_PORT}", "info")
    print_status(f"Frontend: Check Vite output for URL (usually http://localhost:5173)", "info")
    print_status("Press Ctrl+C to shut down both servers.\n", "warning")
    
    return processes

def cleanup(processes):
    """Terminate processes gracefully."""
    print_status("\nShutting down...", "info")
    for name, p in processes:
        if p.poll() is None:
            print_status(f"Stopping {name}...", "info")
            if os.name == 'nt':
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    print_status("All clear. Goodbye!", "success")

def main():
    check_mongodb()
    python_exe = get_python_executable()
    
    # Ask if dependencies should be installed? Or just do it?
    # For a helper script, doing it once is good. If we want speed, we could skip it.
    # Let's check for node_modules to decide.
    if not os.path.exists(os.path.join(CLIENT_DIR, "node_modules")):
        install_dependencies(python_exe)
    else:
        print_status("Node modules found, skipping install. (Run 'npm install' manually in client if needed)", "info")

    processes = start_processes(python_exe)
    
    try:
        while True:
            time.sleep(1)
            for name, p in processes:
                if p.poll() is not None:
                    print_status(f"{name} stopped unexpectedly (Exit code: {p.returncode})", "error")
                    cleanup(processes)
                    return
    except KeyboardInterrupt:
        cleanup(processes)

if __name__ == "__main__":
    main()
