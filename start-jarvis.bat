@echo off

title JARVIS Boot Sequence

set ROOT=%~dp0

echo ======================================
echo         STARTING JARVIS
echo ======================================

echo.
echo [1/3] Starting Ollama...
start "JARVIS Ollama" cmd /k "ollama serve"

timeout /t 3 > nul

echo.
echo [2/3] Starting Backend...
start "JARVIS Backend" cmd /k "cd /d "%ROOT%services\agent-api" && "%ROOT%.venv311\Scripts\activate.bat" && uvicorn main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 8 > nul

echo.
echo [3/3] Starting Desktop App...
start "JARVIS Desktop" cmd /k "cd /d "%ROOT%apps\desktop" && npm run tauri:dev"

echo.
echo ======================================
echo      JARVIS STARTUP COMMANDS SENT
echo ======================================

pause