VOICE_PRESETS = {
    "speak diagnostics": "Running full system diagnostics now.",
    "speak status": "All primary systems appear operational.",
    "speak daily summary": "Preparing your daily operational summary.",
    "speak workflow": "Reviewing your active workflow and tasks.",
    "speak screen analysis": "Analyzing current screen contents now.",
}


def get_voice_preset(command):
    command = command.strip().lower()

    if command not in VOICE_PRESETS:
        return {
            "success": False,
            "error": "Unknown voice preset.",
        }

    return {
        "success": True,
        "command": command,
        "response": VOICE_PRESETS[command],
    }


def format_voice_preset(result):
    if not result.get("success"):
        return (
            "VOICE PRESET ERROR\n\n"
            f"{result.get('error')}"
        )

    return (
        "VOICE COMMAND PRESET\n\n"
        f"Command: {result.get('command')}\n\n"
        f"{result.get('response')}"
    )