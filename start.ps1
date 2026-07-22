# ============================================================
#  AI Learning Coach - Local Startup Script (PowerShell)
#  Usage: Right-click -> "Run with PowerShell"
#         OR in terminal: .\start.ps1
# ============================================================

param(
    [int]$Port = 8000,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

$Root    = $PSScriptRoot
$Backend = Join-Path $Root "backend"
$Venv    = Join-Path $Root ".venv"
$Python  = Join-Path $Venv "Scripts\python.exe"
$Pip     = Join-Path $Venv "Scripts\pip.exe"

Write-Host ""
Write-Host " ================================================" -ForegroundColor Cyan
Write-Host "  AI Learning Coach & Interview Guide"            -ForegroundColor White
Write-Host "  Local Development Server"                       -ForegroundColor Gray
Write-Host " ================================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check virtual environment ────────────────────────────
if (-not (Test-Path $Python)) {
    Write-Host "[ERROR] Virtual environment not found at .venv\" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Run these commands first:" -ForegroundColor Yellow
    Write-Host "    python -m venv .venv"
    Write-Host "    .venv\Scripts\pip install -r backend\requirements.txt"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# ── 2. Install / update dependencies ────────────────────────
Write-Host "[1/3] Verifying dependencies..." -ForegroundColor Yellow
$req = Join-Path $Backend "requirements.txt"
& $Pip install -r $req --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Dependency install failed. Check backend\requirements.txt" -ForegroundColor Red
    exit 1
}
Write-Host "       OK" -ForegroundColor Green

# ── 3. Open browser (non-blocking) ──────────────────────────
if (-not $NoBrowser) {
    Write-Host "[2/3] Browser will open at http://127.0.0.1:$Port in 3 seconds..." -ForegroundColor Yellow
    Start-Job -ScriptBlock {
        param($url)
        Start-Sleep 3
        Start-Process $url
    } -ArgumentList "http://127.0.0.1:$Port" | Out-Null
}

# ── 4. Start uvicorn from backend directory ──────────────────
Write-Host "[3/3] Starting server on http://127.0.0.1:$Port" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host "  ────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""

Push-Location $Backend
try {
    & $Python -m uvicorn app.main:app --host 127.0.0.1 --port $Port --reload
} finally {
    Pop-Location
}
