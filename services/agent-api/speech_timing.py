def estimate_speech_timing(text):
    text = str(text)

    words = text.split()

    word_count = len(words)

    estimated_seconds = round(word_count / 2.5, 2)

    if word_count < 20:
        intensity = "low"
    elif word_count < 80:
        intensity = "medium"
    else:
        intensity = "high"

    return {
        "success": True,
        "word_count": word_count,
        "estimated_seconds": estimated_seconds,
        "intensity": intensity,
    }


def format_speech_timing(result):
    if not result.get("success"):
        return (
            "SPEECH TIMING FAILED\n\n"
            f"{result.get('error')}"
        )

    return (
        "SPEECH TIMING ESTIMATE\n\n"
        f"Words: {result.get('word_count')}\n"
        f"Estimated duration: {result.get('estimated_seconds')} seconds\n"
        f"Intensity: {result.get('intensity')}"
    )