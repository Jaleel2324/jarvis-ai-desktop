import os


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

BACKEND_PATH = os.path.join(
    PROJECT_ROOT,
    "services",
    "agent-api"
)

FRONTEND_PATH = os.path.join(
    PROJECT_ROOT,
    "apps",
    "desktop"
)


def get_launch_help():
    return f"""
JARVIS LAUNCH COMMANDS

BACKEND TERMINAL:
cd "{BACKEND_PATH}"
python -m uvicorn main:app --reload --port 8000

FRONTEND TERMINAL:
cd "{FRONTEND_PATH}"
npm run tauri dev

ONE-CLICK LAUNCH:
Double-click start-jarvis.bat in the jarvis-os folder.
"""