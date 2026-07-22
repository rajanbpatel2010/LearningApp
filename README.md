# Learning Coach

A lightweight AI-powered learning and interview coaching prototype with:

- FastAPI backend with authentication and orchestration
- SQLite-backed knowledge and question management
- A simple browser UI for coaching, uploads, and management

## Run locally

1. Open the backend folder:
   ```powershell
   cd backend
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   python -m pip install python-multipart
   ```
3. Start the server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
4. Open the app in your browser at:
   ```text
   http://127.0.0.1:8000/
   ```
