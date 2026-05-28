import os
import subprocess
import requests

from datetime import datetime


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "logs",
    "jarvis_actions.log"
)


def check_ollama_status():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3
        )

        return response.status_code == 200

    except Exception:
        return False


def restart_ollama():
    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", "ollama", "serve"],
            shell=True
        )

        return {
            "success": True,
            "message": "Ollama restart command sent."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def scan_logs_for_errors(limit: int = 120):
    if not os.path.exists(LOG_FILE):
        return {
            "success": True,
            "message": "No log file found yet.",
            "errors": []
        }

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        lines = file.readlines()

    recent = lines[-limit:]

    error_lines = [
        line.strip()
        for line in recent
        if "ERROR" in line.upper()
        or "FAILED" in line.upper()
        or "TRACEBACK" in line.upper()
    ]

    return {
        "success": True,
        "message": f"Scanned last {len(recent)} log lines.",
        "errors": error_lines[:30]
    }


def repair_voice():
    checks = []

    try:
        import tts_engine

        checks.append(
            "TTS engine import successful."
        )

    except Exception as e:
        return {
            "success": False,
            "message": (
                "Voice repair check failed. "
                f"TTS engine could not import: {e}"
            )
        }

    ffmpeg_path = getattr(
        tts_engine,
        "FFMPEG_PATH",
        ""
    )

    if ffmpeg_path and os.path.exists(ffmpeg_path):
        checks.append(
            f"FFmpeg found: {ffmpeg_path}"
        )
    else:
        checks.append(
            "FFmpeg path missing or invalid."
        )

    return {
        "success": True,
        "message": "Voice system checked.",
        "checks": checks
    }


def restart_frontend():
    frontend_path = os.path.join(
        PROJECT_ROOT,
        "apps",
        "desktop"
    )

    try:
        subprocess.Popen(
            [
                "powershell",
                "-NoExit",
                "-Command",
                f'cd "{frontend_path}"; npm run tauri:dev'
            ],
            shell=True
        )

        return {
            "success": True,
            "message": "Frontend restart command sent."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def run_recovery_action(action: str):
    lower = action.lower().strip()

    if lower in [
        "restart ollama",
        "repair ollama"
    ]:
        return restart_ollama()

    if lower in [
        "repair voice",
        "check voice"
    ]:
        return repair_voice()

    if lower in [
        "scan logs",
        "scan logs for errors"
    ]:
        return scan_logs_for_errors()

    if lower in [
        "restart frontend",
        "relaunch frontend"
    ]:
        return restart_frontend()

    return {
        "success": False,
        "message": f"Unknown recovery action: {action}"
    }


def format_recovery_result(action: str):
    result = run_recovery_action(action)

    lines = [
        "JARVIS RECOVERY REPORT",
        "",
        f"Action: {action}",
        f"Timestamp: {datetime.now().isoformat()}",
        f"Success: {result.get('success')}",
        "",
        result.get("message", ""),
    ]

    if result.get("checks"):
        lines.append("")
        lines.append("CHECKS")

        for check in result["checks"]:
            lines.append(f"- {check}")

    if result.get("errors"):
        lines.append("")
        lines.append("RECENT ERRORS")

        for error in result["errors"]:
            lines.append(f"- {error}")

    return "\n".join(lines)