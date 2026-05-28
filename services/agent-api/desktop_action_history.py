import json
import os
from datetime import datetime

HISTORY_FILE = "desktop_action_history.json"


def load_action_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_action_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def remember_executed_action(
    action,
    success=True,
    result_message=None,
):
    history = load_action_history()

    entry = {
        "id": len(history) + 1,
        "timestamp": datetime.now().isoformat(),
        "success": success,
        "message": result_message,
        "action": action,
    }

    history.append(entry)

    history = history[-500:]

    save_action_history(history)

    return {
        "success": True,
        "entry": entry,
        "history_count": len(history),
    }


def get_action_history(limit=25):
    history = load_action_history()

    history = list(reversed(history))

    return {
        "success": True,
        "history": history[:limit],
    }


def clear_action_history():
    save_action_history([])

    return {
        "success": True,
        "message": "Desktop action history cleared.",
    }


def format_action_history(result):
    if not result.get("success"):
        return (
            "DESKTOP ACTION HISTORY ERROR\n\n"
            f"{result.get('error')}"
        )

    history = result.get("history", [])

    if not history:
        return "Desktop action history is empty."

    lines = [
        "DESKTOP ACTION HISTORY",
        "",
        f"Entries: {len(history)}",
        "",
    ]

    for item in history:
        lines.append(f"ID: {item.get('id')}")
        lines.append(f"Time: {item.get('timestamp')}")
        lines.append(f"Success: {item.get('success')}")
        lines.append(f"Message: {item.get('message')}")
        lines.append(f"Action: {item.get('action')}")
        lines.append("")

    return "\n".join(lines)


def format_action_history_save(result):
    if not result.get("success"):
        return (
            "DESKTOP ACTION HISTORY SAVE FAILED\n\n"
            f"{result.get('error')}"
        )

    return (
        "DESKTOP ACTION SAVED TO HISTORY\n\n"
        f"History count: {result.get('history_count')}\n\n"
        f"Entry: {result.get('entry')}"
    )