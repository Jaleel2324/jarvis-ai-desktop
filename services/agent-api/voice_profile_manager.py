import json
import os
from datetime import datetime

VOICE_PROFILE_FILE = "jarvis_voice_profile.json"

DEFAULT_PROFILE = {
    "voice_name": "JARVIS",
    "tone": "cinematic",
    "emotion": "controlled",
    "speech_speed": "medium",
    "verbosity": "balanced",
    "response_style": "cinematic_assistant",
    "updated_at": None,
}


def load_voice_profile():
    if not os.path.exists(VOICE_PROFILE_FILE):
        save_voice_profile(DEFAULT_PROFILE.copy())
        return DEFAULT_PROFILE.copy()

    try:
        with open(VOICE_PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return DEFAULT_PROFILE.copy()


def save_voice_profile(profile):
    profile["updated_at"] = datetime.now().isoformat()

    with open(VOICE_PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=2)


def update_voice_profile(key, value):
    profile = load_voice_profile()

    profile[key] = value

    save_voice_profile(profile)

    return {
        "success": True,
        "profile": profile,
        "updated_key": key,
        "updated_value": value,
    }


def get_voice_profile():
    return {
        "success": True,
        "profile": load_voice_profile(),
    }


def format_voice_profile(result):
    if not result.get("success"):
        return (
            "VOICE PROFILE ERROR\n\n"
            f"{result.get('error')}"
        )

    profile = result.get("profile", {})

    lines = [
        "JARVIS VOICE PROFILE",
        "",
    ]

    for key, value in profile.items():
        lines.append(f"{key}: {value}")

    return "\n".join(lines)