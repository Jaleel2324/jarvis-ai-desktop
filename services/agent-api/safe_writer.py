import os

from ai_file_editor import improve_file_with_ai
from file_backup import backup_file
from rollback_manager import rollback_file
from syntax_checker import validate_file_syntax


def safe_ai_edit(
    path: str,
    instruction: str
):
    backup = backup_file(path)

    if not backup["success"]:
        return {
            "success": False,
            "error": backup["error"]
        }

    result = improve_file_with_ai(
        path,
        instruction
    )

    if not result["success"]:
        rollback_file(
            os.path.basename(
                backup["backup"]
            ),
            path
        )

        return {
            "success": False,
            "error": result["error"],
            "backup": backup["backup"],
            "rolled_back": True
        }

    syntax = validate_file_syntax(path)

    if not syntax["success"]:
        rollback_file(
            os.path.basename(
                backup["backup"]
            ),
            path
        )

        return {
            "success": False,
            "error": (
                "Syntax validation failed. "
                "The file was automatically rolled back.\n\n"
                f"{syntax['output']}"
            ),
            "backup": backup["backup"],
            "rolled_back": True
        }

    return {
        "success": True,
        "path": path,
        "backup": backup["backup"],
        "syntax": syntax["output"],
        "rolled_back": False
    }