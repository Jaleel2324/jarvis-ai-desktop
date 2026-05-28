import os

from datetime import datetime


LOG_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "logs",
    )
)

LOG_FILE = os.path.join(
    LOG_ROOT,
    "jarvis_actions.log"
)


def ensure_log_dir():
    os.makedirs(
        LOG_ROOT,
        exist_ok=True
    )


def log_action(
    action: str,
    details: str = ""
):
    ensure_log_dir()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    entry = (
        f"[{timestamp}] {action}\n"
        f"{details}\n"
        "----------------------------------------\n"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(entry)

    return {
        "success": True,
        "log_file": LOG_FILE,
    }


def read_recent_logs(limit: int = 80):
    ensure_log_dir()

    if not os.path.exists(LOG_FILE):
        return "No JARVIS logs found yet."

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        lines = file.readlines()

    recent = lines[-limit:]

    return "".join(recent)