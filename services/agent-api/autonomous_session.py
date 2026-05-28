import json
import os
from datetime import datetime


SESSION_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory"
)

SESSION_FILE = os.path.join(
    SESSION_DIR,
    "autonomous_session.json"
)


def ensure_session_dir():
    os.makedirs(SESSION_DIR, exist_ok=True)


def save_autonomous_session(goal: str, plan: dict):
    ensure_session_dir()

    session = {
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "goal": goal,
        "status": "planned",
        "current_step": 0,
        "completed_steps": [],
        "failed_steps": [],
        "edited_files": [],
        "plan": plan,
    }

    with open(SESSION_FILE, "w", encoding="utf-8") as file:
        json.dump(session, file, indent=2)

    return session


def load_autonomous_session():
    ensure_session_dir()

    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def update_autonomous_session(session: dict):
    ensure_session_dir()

    session["updated_at"] = datetime.now().isoformat()

    with open(SESSION_FILE, "w", encoding="utf-8") as file:
        json.dump(session, file, indent=2)

    return session


def clear_autonomous_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

    return True


def format_autonomous_session():
    session = load_autonomous_session()

    if not session:
        return "No autonomous session found."

    plan = session.get("plan", {})
    steps = plan.get("steps", [])

    step_text = "\n".join(
        [
            f"{step.get('step', index + 1)}. {step.get('title', 'Untitled step')}"
            for index, step in enumerate(steps)
        ]
    )

    return (
        "JARVIS AUTONOMOUS SESSION\n\n"
        f"Goal: {session.get('goal')}\n"
        f"Status: {session.get('status')}\n"
        f"Current Step: {session.get('current_step')}\n\n"
        "Steps:\n"
        f"{step_text or '- No steps saved'}"
    )