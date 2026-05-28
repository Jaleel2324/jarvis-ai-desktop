from file_backup import list_backups, restore_backup


def show_backups():
    backups = list_backups()

    if not backups:
        return "No backups found."

    return "AVAILABLE BACKUPS\n\n" + "\n".join(
        f"- {backup}" for backup in backups
    )


def rollback_file(backup_name: str, target_path: str):
    result = restore_backup(
        backup_name,
        target_path
    )

    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }

    return {
        "success": True,
        "message": (
            "Rollback completed.\n\n"
            f"Backup used: {result['backup_used']}\n"
            f"Restored to: {result['restored_to']}"
        )
    }