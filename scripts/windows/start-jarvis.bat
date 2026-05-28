@echo off
cd /d "%~dp0"

echo Starting JARVIS...

start "JARVIS Backend" powershell -NoExit -ExecutionPolicy Bypass -File ".\start-backend.ps1"

timeout /t 15

start "JARVIS Frontend" powershell -NoExit -ExecutionPolicy Bypass -File ".\start-frontend.ps1"

echo Done.
pause