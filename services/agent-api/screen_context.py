import os
from datetime import datetime

from openai import OpenAI

from screen_capture import capture_screen


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


SCREEN_CONTEXT_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory/screen_context"
)


def ensure_screen_context_dir():
    os.makedirs(SCREEN_CONTEXT_DIR, exist_ok=True)


def describe_latest_screen():
    ensure_screen_context_dir()

    capture = capture_screen()

    if not capture.get("success"):
        return {
            "success": False,
            "error": capture.get("error", "Screen capture failed."),
        }

    prompt = f"""
You are JARVIS, a desktop screen awareness assistant.

A screenshot was captured and saved here:

{capture.get("path")}

You currently cannot visually inspect the image directly from this function.
Your job is to create a useful screen context note based on the saved screenshot metadata.

Return a concise response explaining:
- screenshot path
- capture time
- what the user should do next if they want detailed visual analysis
- how this screenshot can be used for future vision/OCR features
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a helpful local desktop assistant. "
                    "Be clear, practical, and concise."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    description = response.choices[0].message.content

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    context_file = os.path.join(
        SCREEN_CONTEXT_DIR,
        f"screen_context_{timestamp}.txt"
    )

    with open(context_file, "w", encoding="utf-8") as file:
        file.write(description)

    return {
        "success": True,
        "capture": capture,
        "description": description,
        "context_file": context_file,
        "created_at": datetime.now().isoformat(),
    }


def format_screen_context(result: dict):
    if not result.get("success"):
        return (
            "SCREEN CONTEXT FAILED\n\n"
            f"Error: {result.get('error')}"
        )

    capture = result.get("capture", {})

    return (
        "SCREEN CONTEXT CREATED\n\n"
        f"Screenshot: {capture.get('path')}\n"
        f"Context File: {result.get('context_file')}\n"
        f"Created At: {result.get('created_at')}\n\n"
        "JARVIS Notes:\n"
        f"{result.get('description')}"
    )