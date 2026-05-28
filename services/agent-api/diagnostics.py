import os
import time
import sqlite3
import requests

from datetime import datetime

from system_monitor import get_system_status


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "jarvis_memory.db"
)

LOGS_PATH = os.path.join(
    PROJECT_ROOT,
    "logs"
)

BACKUPS_PATH = os.path.join(
    PROJECT_ROOT,
    "backups"
)

TASK_LOGS_PATH = os.path.join(
    PROJECT_ROOT,
    "task-logs"
)


def check_ollama():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3
        )

        return {
            "name": "Ollama",
            "status": "online" if response.status_code == 200 else "warning",
            "details": f"HTTP {response.status_code}"
        }

    except Exception as e:
        return {
            "name": "Ollama",
            "status": "offline",
            "details": str(e)
        }


def check_database():
    try:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

        tables = cursor.fetchall()

        connection.close()

        return {
            "name": "Memory Database",
            "status": "online",
            "details": f"{len(tables)} table(s) found"
        }

    except Exception as e:
        return {
            "name": "Memory Database",
            "status": "error",
            "details": str(e)
        }


def check_folder(name: str, path: str):
    try:
        os.makedirs(
            path,
            exist_ok=True
        )

        return {
            "name": name,
            "status": "online",
            "details": path
        }

    except Exception as e:
        return {
            "name": name,
            "status": "error",
            "details": str(e)
        }


def check_tts():
    try:
        import tts_engine

        return {
            "name": "TTS Engine",
            "status": "online",
            "details": "XTTS module loaded"
        }

    except Exception as e:
        return {
            "name": "TTS Engine",
            "status": "error",
            "details": str(e)
        }


def run_diagnostics():
    started = time.time()

    checks = [
        check_ollama(),
        check_database(),
        check_tts(),
        check_folder("Logs Folder", LOGS_PATH),
        check_folder("Backups Folder", BACKUPS_PATH),
        check_folder("Task Logs Folder", TASK_LOGS_PATH),
    ]

    system = get_system_status()

    passed = len([
        check for check in checks
        if check["status"] == "online"
    ])

    warnings = len([
        check for check in checks
        if check["status"] == "warning"
    ])

    failed = len([
        check for check in checks
        if check["status"] in ["offline", "error"]
    ])

    return {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": round(time.time() - started, 2),
        "summary": {
            "passed": passed,
            "warnings": warnings,
            "failed": failed,
        },
        "checks": checks,
        "system": system,
    }


def format_diagnostics_report():
    result = run_diagnostics()

    lines = [
        "JARVIS SELF-DIAGNOSTIC REPORT",
        "",
        f"Timestamp: {result['timestamp']}",
        f"Duration: {result['duration_seconds']}s",
        "",
        "SUMMARY",
        f"Passed: {result['summary']['passed']}",
        f"Warnings: {result['summary']['warnings']}",
        f"Failed: {result['summary']['failed']}",
        "",
        "SYSTEM",
        f"Node: {result['system']['node']}",
        f"OS: {result['system']['system']}",
        f"CPU: {result['system']['cpu_percent']}%",
        f"Memory: {result['system']['memory_percent']}%",
        f"Disk: {result['system']['disk_percent']}%",
        "",
        "CHECKS",
    ]

    for check in result["checks"]:
        status = check["status"].upper()

        lines.append(
            f"[{status}] {check['name']} — {check['details']}"
        )

    if result["summary"]["failed"] == 0:
        lines.append("")
        lines.append("Overall Status: JARVIS systems are operational.")
    else:
        lines.append("")
        lines.append("Overall Status: JARVIS detected issues requiring attention.")

    return "\n".join(lines)