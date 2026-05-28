import os
import shutil

from datetime import datetime


BACKUP_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "backups",
    )
)


def ensure_backup_dir():
    os.makedirs(
        BACKUP_ROOT,
        exist_ok=True
    )


def backup_file(path: str):
    ensure_backup_dir()

    if not os.path.exists(path):
        return {
            "success": False,
            "error": "File does not exist."
        }

    filename = os.path.basename(path)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_name = (
        f"{timestamp}_{filename}"
    )

    backup_path = os.path.join(
        BACKUP_ROOT,
        backup_name
    )

    shutil.copy2(
        path,
        backup_path
    )

    return {
        "success": True,
        "original": path,
        "backup": backup_path
    }


def list_backups():
    ensure_backup_dir()

    files = sorted(
        os.listdir(BACKUP_ROOT),
        reverse=True
    )

    return files[:100]


def restore_backup(
    backup_name: str,
    target_path: str
):
    ensure_backup_dir()

    backup_path = os.path.join(
        BACKUP_ROOT,
        backup_name
    )

    if not os.path.exists(backup_path):
        return {
            "success": False,
            "error": "Backup not found."
        }

    shutil.copy2(
        backup_path,
        target_path
    )

    return {
        "success": True,
        "restored_to": target_path,
        "backup_used": backup_path
    }