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
set "PORT=8000"

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

:: ── Kill any existing process on the port ─────────────────
echo [2/3] Checking port %PORT%...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":%PORT% " ^| findstr "LISTENING"') do (
    echo        Port %PORT% is in use by PID %%a, releasing it...
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 1 /nobreak >nul
)
echo        Port %PORT% is ready. Starting server...
echo        URL: http://127.0.0.1:%PORT%
echo.

:: ── Verify uvicorn is importable before launching ──────────
"%PYTHON%" -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] uvicorn is not installed in the virtual environment.
    echo  Run: .venv\Scripts\pip install uvicorn
    pause
    exit /b 1
)

:: ── Open browser after 3 second delay ─────────────────────
echo [3/3] Opening browser in 3 seconds...
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:%PORT%"

:: ── Launch uvicorn from the backend directory ─────────────
cd /d "%BACKEND%"
echo.
echo  Press Ctrl+C to stop the server.
echo  ────────────────────────────────────────────────
"%PYTHON%" -m uvicorn app.main:app --host 127.0.0.1 --port %PORT% --reload

:: Uvicorn exits with non-zero when stopped via Ctrl+C (normal).
:: Only pause and show error if it exits unexpectedly fast.
if %errorlevel% GTR 1 (
    echo.
    echo [ERROR] Server exited unexpectedly (code %errorlevel%). Check the output above.
    pause
)

endlocal
