import os
from datetime import datetime

from PIL import Image
import pytesseract

from screen_capture import capture_screen


OCR_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory/screen_ocr"
)


def ensure_ocr_dir():
    os.makedirs(OCR_DIR, exist_ok=True)


def read_screen_text():
    ensure_ocr_dir()

    capture = capture_screen()

    if not capture.get("success"):
        return {
            "success": False,
            "error": capture.get("error", "Screen capture failed."),
        }

    image_path = capture.get("path")

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            OCR_DIR,
            f"screen_ocr_{timestamp}.txt"
        )

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)

        return {
            "success": True,
            "screenshot": image_path,
            "text": text.strip(),
            "ocr_file": output_file,
            "created_at": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "screenshot": image_path,
        }


def format_screen_ocr(result: dict):
    if not result.get("success"):
        return (
            "SCREEN OCR FAILED\n\n"
            f"Error: {result.get('error')}\n"
            f"Screenshot: {result.get('screenshot')}"
        )

    text = result.get("text") or "No text detected."

    return (
        "SCREEN OCR COMPLETE\n\n"
        f"Screenshot: {result.get('screenshot')}\n"
        f"OCR File: {result.get('ocr_file')}\n"
        f"Created At: {result.get('created_at')}\n\n"
        "Detected Text:\n"
        f"{text[:4000]}"
    )