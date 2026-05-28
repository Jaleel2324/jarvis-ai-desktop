import json
import os
from datetime import datetime

PROJECT_STATE_FILE = "jarvis_project_state.json"

DEFAULT_STATE = {
    "current_phase": "Phase 16 — Real Memory System",
    "last_working_backend_command": "python main.py",
    "last_working_frontend_command": "npm run tauri dev",
    "current_focus": "Build long-term memory, conversation recall, and context injection.",
    "known_blockers": [],
    "updated_at": None,
}


def load_project_state():
    if not os.path.exists(PROJECT_STATE_FILE):
        save_project_state(DEFAULT_STATE.copy())
        return DEFAULT_STATE.copy()

    try:
        with open(PROJECT_STATE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else DEFAULT_STATE.copy()
    except Exception:
        return DEFAULT_STATE.copy()


def save_project_state(state):
    state["updated_at"] = datetime.now().isoformat()

    with open(PROJECT_STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def update_project_state(key, value):
    state = load_project_state()
    state[key] = value
    save_project_state(state)

    return {
        "success": True,
        "state": state,
        "updated_key": key,
        "updated_value": value,
    }


def add_project_blocker(blocker):
    state = load_project_state()
    blockers = state.get("known_blockers", [])

    blockers.append({
        "timestamp": datetime.now().isoformat(),
        "blocker": blocker,
    })

    state["known_blockers"] = blockers[-50:]
    save_project_state(state)

    return {"success": True, "state": state, "blocker": blocker}


def get_project_state():
    return {"success": True, "state": load_project_state()}


def format_project_state(result):
    if not result.get("success"):
        return "PROJECT STATE FAILED\n\n" + str(result.get("error"))

    state = result.get("state", {})

    lines = [
        "JARVIS PROJECT STATE",
        "",
        f"Current phase: {state.get('current_phase')}",
        f"Current focus: {state.get('current_focus')}",
        f"Backend command: {state.get('last_working_backend_command')}",
        f"Frontend command: {state.get('last_working_frontend_command')}",
        f"Updated: {state.get('updated_at')}",
        "",
        "Known blockers:",
    ]

    blockers = state.get("known_blockers", [])

    if not blockers:
        lines.append("- None")
    else:
        for item in blockers[-10:]:
            lines.append(f"- {item.get('blocker')} ({item.get('timestamp')})")

    return "\n".join(lines)
