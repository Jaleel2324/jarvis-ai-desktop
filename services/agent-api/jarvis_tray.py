import subprocess
import sys
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
except Exception:
    pystray = None
    Image = None
    ImageDraw = None


def create_icon_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, 54, 54), outline="cyan", width=4)
    draw.ellipse((24, 24, 40, 40), fill="cyan")
    return image


def run_launcher():
    current_dir = Path(__file__).resolve().parent
    subprocess.Popen(
        [sys.executable, "production_launcher.py"],
        cwd=str(current_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def open_status():
    current_dir = Path(__file__).resolve().parent
    command = (
        "from process_manager import get_service_status, format_service_status; "
        "print(format_service_status(get_service_status())); "
        "input('Press Enter to close...')"
    )

    subprocess.Popen(
        [sys.executable, "-c", command],
        cwd=str(current_dir),
    )


def quit_tray(icon):
    icon.stop()


def run_tray():
    if pystray is None:
        print("pystray is not installed. Run: pip install pystray pillow")
        return

    icon = pystray.Icon(
        "JARVIS",
        create_icon_image(),
        "JARVIS",
        menu=pystray.Menu(
            pystray.MenuItem("Start / Recover JARVIS", lambda: run_launcher()),
            pystray.MenuItem("Show Status", lambda: open_status()),
            pystray.MenuItem("Quit Tray", quit_tray),
        ),
    )

    icon.run()


if __name__ == "__main__":
    run_tray()
