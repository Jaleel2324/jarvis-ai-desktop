cd "$HOME\OneDrive\Desktop\jarvis-os\services\agent-api"
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000