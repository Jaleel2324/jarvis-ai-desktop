import os
from pathlib import Path

STARTUP_FILE_NAME = "Start_JARVIS.bat"


def get_startup_folder():
    if os.name != "nt":
        return None

    appdata = os.environ.get("APPDATA")

    if not appdata:
        return None

    return os.path.join(
        appdata,
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )


def create_startup_script(project_root=None):
    if os.name != "nt":
        return {
            "success": False,
            "error": "Windows startup script is only supported on Windows.",
        }

    startup_folder = get_startup_folder()

    if not startup_folder:
        return {
            "success": False,
            "error": "Could not locate Windows Startup folder.",
        }

    os.makedirs(startup_folder, exist_ok=True)

    if project_root is None:
        project_root = Path(__file__).resolve().parents[2]

    project_root = Path(project_root).resolve()
    script_path = os.path.join(startup_folder, STARTUP_FILE_NAME)

    launcher_path = project_root / "services" / "agent-api" / "production_launcher.py"

    bat_content = (
        '@echo off\n'
        f'cd /d "{launcher_path.parent}"\n'
        'python production_launcher.py\n'
    )

    with open(script_path, "w", encoding="utf-8") as file:
        file.write(bat_content)

    return {
        "success": True,
        "message": "JARVIS startup script created.",
        "startup_script": script_path,
        "launcher": str(launcher_path),
    }


def remove_startup_script():
    startup_folder = get_startup_folder()

    if not startup_folder:
        return {
            "success": False,
            "error": "Could not locate Windows Startup folder.",
        }

    script_path = os.path.join(startup_folder, STARTUP_FILE_NAME)

    if os.path.exists(script_path):
        os.remove(script_path)

    return {
        "success": True,
        "message": "JARVIS startup script removed.",
        "startup_script": script_path,
    }


def check_startup_script():
    startup_folder = get_startup_folder()

    if not startup_folder:
        return {
            "success": False,
            "error": "Could not locate Windows Startup folder.",
            "enabled": False,
        }

    script_path = os.path.join(startup_folder, STARTUP_FILE_NAME)

    return {
        "success": True,
        "enabled": os.path.exists(script_path),
        "startup_script": script_path,
    }


def format_startup_result(result):
    if not result.get("success"):
        return (
            "JARVIS STARTUP MANAGER ERROR\n\n"
            f"{result.get('error')}"
        )

    lines = [
        "JARVIS STARTUP MANAGER",
        "",
        f"Message: {result.get('message', '')}",
        f"Enabled: {result.get('enabled', '')}",
        f"Startup script: {result.get('startup_script', '')}",
        f"Launcher: {result.get('launcher', '')}",
    ]

    return "\n".join(lines)
