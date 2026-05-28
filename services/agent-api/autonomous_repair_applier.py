from datetime import datetime

from autonomous_session import (
    load_autonomous_session,
    update_autonomous_session,
)

from autonomous_validator import run_autonomous_validation

from safe_writer import safe_ai_edit

from rollback_manager import rollback_file


def apply_autonomous_repair():
    session = load_autonomous_session()

    if not session:
        return {
            "success": False,
            "error": "No autonomous session found.",
        }

    repair_plan = session.get("last_repair_plan")

    if not repair_plan:
        return {
            "success": False,
            "error": "No repair plan found. Run: plan autonomous repair",
        }

    recommended_repairs = repair_plan.get("recommended_repairs", [])

    if not recommended_repairs:
        return {
            "success": False,
            "error": "Repair plan contains no recommended repairs.",
        }

    applied_repairs = []
    rollback_targets = []
    skipped_repairs = []

    for repair in recommended_repairs:
        repair_type = repair.get("repair_type")
        target_files = repair.get("target_files", [])
        description = repair.get("description", "")

        if repair_type != "safe_edit":
            skipped_repairs.append({
                "title": repair.get("title", "Untitled repair"),
                "reason": f"Skipped repair type: {repair_type}",
            })
            continue

        if not target_files:
            skipped_repairs.append({
                "title": repair.get("title", "Untitled repair"),
                "reason": "No target files listed.",
            })
            continue

        for path in target_files:
            result = safe_ai_edit(
                path,
                description,
            )

            if not result.get("success"):
                rollback_errors = []

                for rollback_item in rollback_targets:
                    try:
                        rollback_file(
                            rollback_item["backup"],
                            rollback_item["path"],
                        )
                    except Exception as rollback_error:
                        rollback_errors.append(str(rollback_error))

                session["status"] = "repair_failed"
                session["last_repair_failed_at"] = datetime.now().isoformat()
                update_autonomous_session(session)

                return {
                    "success": False,
                    "error": result.get("error", "Unknown repair failure."),
                    "failed_repair": repair,
                    "failed_file": path,
                    "rollback_errors": rollback_errors,
                    "skipped_repairs": skipped_repairs,
                }

            applied_repairs.append({
                "title": repair.get("title", "Untitled repair"),
                "path": path,
                "backup": result.get("backup"),
                "syntax": result.get("syntax"),
            })

            rollback_targets.append({
                "path": path,
                "backup": result.get("backup"),
            })

    if not applied_repairs:
        session["status"] = "repair_skipped"
        session["last_repair_skipped_at"] = datetime.now().isoformat()
        update_autonomous_session(session)

        return {
            "success": False,
            "error": (
                "No repairs were applied. "
                "Only repair_type='safe_edit' repairs are applied automatically."
            ),
            "skipped_repairs": skipped_repairs,
        }

    validation_result = run_autonomous_validation()

    if not validation_result.get("success"):
        rollback_errors = []

        for rollback_item in rollback_targets:
            try:
                rollback_file(
                    rollback_item["backup"],
                    rollback_item["path"],
                )
            except Exception as rollback_error:
                rollback_errors.append(str(rollback_error))

        session["status"] = "repair_validation_failed"
        session["last_repair_validation_failed_at"] = datetime.now().isoformat()
        update_autonomous_session(session)

        return {
            "success": False,
            "error": "Validation failed after repair application.",
            "validation": validation_result,
            "rollback_errors": rollback_errors,
            "applied_repairs": applied_repairs,
            "skipped_repairs": skipped_repairs,
        }

    edited_files = session.get("edited_files", [])

    for repair in applied_repairs:
        edited_files.append(repair["path"])

    session["edited_files"] = list(set(edited_files))
    session["status"] = "repair_applied"
    session["last_repair_applied_at"] = datetime.now().isoformat()

    update_autonomous_session(session)

    return {
        "success": True,
        "applied_repairs": applied_repairs,
        "skipped_repairs": skipped_repairs,
        "validation": validation_result,
        "session": session,
    }


def format_repair_application(result: dict):
    if not result.get("success"):
        rollback_errors = result.get("rollback_errors", [])
        skipped = result.get("skipped_repairs", [])

        rollback_text = "\n".join(
            [f"- {item}" for item in rollback_errors]
        )

        skipped_text = "\n".join(
            [
                (
                    f"- {item.get('title', 'Untitled repair')}\n"
                    f"  Reason: {item.get('reason', 'No reason provided')}"
                )
                for item in skipped
            ]
        )

        return (
            "AUTONOMOUS REPAIR FAILED\n\n"
            f"Error:\n{result.get('error')}\n\n"
            "Skipped Repairs:\n"
            f"{skipped_text or '- None'}\n\n"
            "Rollback Errors:\n"
            f"{rollback_text or '- None'}"
        )

    applied_repairs = result.get("applied_repairs", [])
    skipped = result.get("skipped_repairs", [])

    applied_text = "\n".join(
        [
            (
                f"- {item.get('title', 'Untitled repair')}\n"
                f"  File: {item.get('path')}\n"
                f"  Backup: {item.get('backup')}\n"
                f"  Syntax: {item.get('syntax') or 'Passed'}"
            )
            for item in applied_repairs
        ]
    )

    skipped_text = "\n".join(
        [
            (
                f"- {item.get('title', 'Untitled repair')}\n"
                f"  Reason: {item.get('reason', 'No reason provided')}"
            )
            for item in skipped
        ]
    )

    return (
        "AUTONOMOUS REPAIR APPLIED\n\n"
        "Applied Repairs:\n"
        f"{applied_text or '- None'}\n\n"
        "Skipped Repairs:\n"
        f"{skipped_text or '- None'}\n\n"
        "Validation:\n"
        "PASSED\n\n"
        "Autonomous session updated successfully."
    )