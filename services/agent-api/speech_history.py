import json
import os
from datetime import datetime

SPEECH_HISTORY_FILE = "speech_history.json"


def load_speech_history():
    if not os.path.exists(SPEECH_HISTORY_FILE):
        return []

    try:
        with open(SPEECH_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_speech_history(history):
    with open(SPEECH_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def remember_spoken_response(text, tone="cinematic", category="general"):
    history = load_speech_history()

    item = {
        "id": len(history) + 1,
        "timestamp": datetime.now().isoformat(),
        "tone": tone,
        "category": category,
        "text": text,
    }

    history.append(item)
    history = history[-200:]

    save_speech_history(history)

    return {
        "success": True,
        "entry": item,
        "count": len(history),
    }


def get_speech_history(limit=25):
    history = list(reversed(load_speech_history()))

    return {
        "success": True,
        "history": history[:limit],
    }


def format_speech_history(result):
    history = result.get("history", [])

    if not history:
        return "No speech history stored."

    lines = ["JARVIS SPEECH HISTORY", ""]

    for item in history:
        lines.append(f"[{item['tone']}] {item['text']}")
        lines.append(f"Time: {item['timestamp']}")
        lines.append("")

    return "\n".join(lines)
