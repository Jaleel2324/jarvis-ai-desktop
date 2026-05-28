import os
from datetime import datetime

from PIL import ImageGrab


SCREENSHOT_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory/screenshots"
)


def ensure_screenshot_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def capture_screen():
    ensure_screenshot_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"screenshot_{timestamp}.png"

    path = os.path.join(
        SCREENSHOT_DIR,
        filename
    )

    image = ImageGrab.grab()
    image.save(path)

    return {
        "success": True,
        "path": path,
        "filename": filename,
        "captured_at": datetime.now().isoformat(),
    }


def format_screen_capture(result: dict):
    if not result.get("success"):
        return (
            "SCREEN CAPTURE FAILED\n\n"
            f"Error: {result.get('error')}"
        )

    return (
        "SCREEN CAPTURE COMPLETE\n\n"
        f"File: {result.get('filename')}\n"
        f"Path: {result.get('path')}\n"
        f"Captured At: {result.get('captured_at')}"
    )