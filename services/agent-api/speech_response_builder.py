import re


def clean_spoken_text(text):
    text = str(text)

    # Remove code blocks so JARVIS does not try to read code aloud
    text = re.sub(
        r"```.*?```",
        "[code omitted for speech]",
        text,
        flags=re.DOTALL,
    )

    # Remove inline markdown/code styling
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"#+ ", "", text)
    text = text.replace("*", "")
    text = text.replace("_", "")

    # Clean whitespace
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_spoken_response(text):
    cleaned = clean_spoken_text(text)

    if len(cleaned) > 500:
        cleaned = cleaned[:500] + "..."

    spoken = cleaned.replace(".", ". ")

    return {
        "success": True,
        "spoken_response": spoken,
        "length": len(spoken),
    }


def format_spoken_response(result):
    if not result.get("success"):
        return (
            "SPOKEN RESPONSE BUILD FAILED\n\n"
            f"{result.get('error')}"
        )

    return (
        "JARVIS SPOKEN RESPONSE\n\n"
        f"{result.get('spoken_response')}"
    )