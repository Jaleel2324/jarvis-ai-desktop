from ai_file_editor import improve_file_with_ai
from file_backup import backup_file
from rollback_manager import rollback_file

import os


def safe_improve_file(path: str, instruction: str):
    backup = backup_file(path)

    if not backup["success"]:
        return {
            "success": False,
            "error": f"Backup failed: {backup['error']}"
        }

    improved = improve_file_with_ai(
        path,
        instruction
    )

    if not improved["success"]:
        rollback_file(
            os.path.basename(backup["backup"]),
            path
        )

        return {
            "success": False,
            "error": improved["error"],
            "backup": backup["backup"],
            "rolled_back": True
        }

    return {
        "success": True,
        "path": path,
        "backup": backup["backup"],
        "rolled_back": False
    }