import os
import sys
import subprocess
import time
import shutil
import webbrowser

PORT = 8050

def main():
    print("=" * 65)
    print(" RideMate - College Auto & Cab Pooling (Hackathon App)")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(base_dir, "backend")
    frontend_dir = os.path.join(base_dir, "frontend")

    # Step 1: Check Node/npm availability
    npm_path = shutil.which("npm") or shutil.which("npm.cmd")
    vite_process = None

    if npm_path:
        node_modules = os.path.join(frontend_dir, "node_modules")
        if not os.path.exists(node_modules):
            print("\nNode environment detected. Installing npm packages...")
            try:
                subprocess.run([npm_path, "install"], cwd=frontend_dir, check=True)
            except Exception as e:
                print(f"Warning during npm install: {e}")

        print("Starting Vite Dev Server on http://localhost:5173 ...")
        try:
            vite_process = subprocess.Popen([npm_path, "run", "dev"], cwd=frontend_dir)
        except Exception as e:
            print(f"Could not start Vite dev server: {e}")
    else:
        print("\nRunning in Zero-Dependency Python Mode (No Node.js required).")

    # Step 2: Start Python FastAPI Backend Server
    print(f"Starting RideMate Python FastAPI App on http://127.0.0.1:{PORT} ...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", "127.0.0.1",
        "--port", str(PORT)
    ]
    
    backend_process = subprocess.Popen(backend_cmd, cwd=backend_dir)

    time.sleep(2.0)

    app_url = f"http://127.0.0.1:{PORT}"
    print("\n" + "=" * 65)
    print(" RideMate Application is running!")
    print(f" Open Web Application:  {app_url}")
    if vite_process:
        print(" Vite Dev Server:        http://localhost:5173")
    print(f" OpenAPI / API Docs:     http://127.0.0.1:{PORT}/docs")
    print("=" * 65)
    print(" Press Ctrl+C to stop the application.\n")

    # Auto-open browser
    try:
        webbrowser.open(app_url)
    except Exception:
        pass

    try:
        backend_process.wait()
        if vite_process:
            vite_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down RideMate server...")
        backend_process.terminate()
        if vite_process:
            vite_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
