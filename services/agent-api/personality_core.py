from voice_profile_manager import load_voice_profile


CINEMATIC_PREFIXES = [
    "Understood.",
    "Running analysis now.",
    "Systems are responding normally.",
    "I have identified the issue.",
    "Processing complete.",
]

TECHNICAL_PREFIXES = [
    "Technical analysis complete.",
    "System diagnostics reviewed.",
    "Backend inspection complete.",
]

CALM_PREFIXES = [
    "Everything appears stable.",
    "No immediate issues detected.",
]

URGENT_PREFIXES = [
    "Attention required.",
    "Critical issue detected.",
]


def apply_personality(text):
    profile = load_voice_profile()
    tone = profile.get("tone", "cinematic")

    prefix = ""

    if tone == "cinematic":
        prefix = CINEMATIC_PREFIXES[0]
    elif tone == "technical":
        prefix = TECHNICAL_PREFIXES[0]
    elif tone == "calm":
        prefix = CALM_PREFIXES[0]
    elif tone == "urgent":
        prefix = URGENT_PREFIXES[0]

    response = f"{prefix} {text}".strip()

    return {
        "success": True,
        "tone": tone,
        "response": response,
    }


def format_personality_result(result):
    if not result.get("success"):
        return (
            "JARVIS PERSONALITY ERROR\n\n"
            f"{result.get('error')}"
        )

    return (
        "JARVIS PERSONALITY OUTPUT\n\n"
        f"Tone: {result.get('tone')}\n\n"
        f"{result.get('response')}"
    )