import json
import os
from datetime import datetime

from screen_ocr import read_screen_text


SCREEN_MEMORY_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory/screen_memory"
)

SCREEN_MEMORY_FILE = os.path.join(
    SCREEN_MEMORY_DIR,
    "screen_memory.json"
)


def ensure_screen_memory_dir():
    os.makedirs(SCREEN_MEMORY_DIR, exist_ok=True)


def load_screen_memory():
    ensure_screen_memory_dir()

    if not os.path.exists(SCREEN_MEMORY_FILE):
        return []

    with open(SCREEN_MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_screen_memory(memory: list):
    ensure_screen_memory_dir()

    with open(SCREEN_MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2)

    return memory


def remember_current_screen():
    memory = load_screen_memory()

    ocr_result = read_screen_text()

    if not ocr_result.get("success"):
        return {
            "success": False,
            "error": ocr_result.get("error"),
            "ocr": ocr_result,
        }

    entry = {
        "created_at": datetime.now().isoformat(),
        "screenshot": ocr_result.get("screenshot"),
        "ocr_file": ocr_result.get("ocr_file"),
        "text": ocr_result.get("text", ""),
    }

    memory.append(entry)

    save_screen_memory(memory)

    return {
        "success": True,
        "entry": entry,
        "total_entries": len(memory),
    }


def summarize_screen_memory():
    memory = load_screen_memory()

    if not memory:
        return {
            "success": True,
            "summary": "No screen memory saved yet.",
            "total_entries": 0,
        }

    latest = memory[-1]

    return {
        "success": True,
        "summary": (
            "SCREEN MEMORY SUMMARY\n\n"
            f"Total Entries: {len(memory)}\n"
            f"Latest Screenshot: {latest.get('screenshot')}\n"
            f"Latest OCR File: {latest.get('ocr_file')}\n"
            f"Latest Time: {latest.get('created_at')}\n\n"
            "Latest Text:\n"
            f"{latest.get('text', '')[:3000] or 'No text detected.'}"
        ),
        "total_entries": len(memory),
        "latest": latest,
    }


def format_screen_memory_save(result: dict):
    if not result.get("success"):
        return (
            "SCREEN MEMORY SAVE FAILED\n\n"
            f"Error: {result.get('error')}"
        )

    entry = result.get("entry", {})

    return (
        "SCREEN MEMORY SAVED\n\n"
        f"Screenshot: {entry.get('screenshot')}\n"
        f"OCR File: {entry.get('ocr_file')}\n"
        f"Saved At: {entry.get('created_at')}\n"
        f"Total Entries: {result.get('total_entries')}"
    )


def format_screen_memory_summary(result: dict):
    return result.get("summary", "No screen memory summary available.")