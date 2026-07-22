@echo off
:: ============================================================
::  AI Learning Coach - Local Startup Script (Windows)
::  Usage: Double-click this file OR run it from the terminal
::  The server is always started from the backend\ directory.
:: ============================================================

setlocal

set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "VENV=%ROOT%.venv"
set "PYTHON=%VENV%\Scripts\python.exe"

echo.
echo  ================================================
echo   AI Learning Coach ^& Interview Guide
echo   Local Development Server
echo  ================================================
echo.

:: ── Check Python venv ──────────────────────────────────────
if not exist "%PYTHON%" (
    echo [ERROR] Virtual environment not found at .venv\
    echo.
    echo  Please run the following commands first:
    echo    python -m venv .venv
    echo    .venv\Scripts\pip install -r backend\requirements.txt
    echo.
    pause
    exit /b 1
)

:: ── Install / verify dependencies ─────────────────────────
echo [1/3] Verifying dependencies...
"%VENV%\Scripts\pip.exe" install -r "%BACKEND%\requirements.txt" --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Check backend\requirements.txt
    pause
    exit /b 1
)
echo        OK

:: ── Detect free port (default 8000) ───────────────────────
set PORT=8000
echo [2/3] Starting server on port %PORT%...
echo        URL: http://127.0.0.1:%PORT%
echo.

:: ── Open browser after 2 second delay ─────────────────────
echo [3/3] Opening browser in 2 seconds...
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://127.0.0.1:%PORT%"

:: ── Launch uvicorn from the backend directory ─────────────
cd /d "%BACKEND%"
echo.
echo  Press Ctrl+C to stop the server.
echo  ────────────────────────────────────────────────
"%VENV%\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port %PORT% --reload

endlocal
