import json
import os
from datetime import datetime

ROUTINES_FILE = "jarvis_routines.json"


def load_routines():
    if not os.path.exists(ROUTINES_FILE):
        return []

    try:
        with open(ROUTINES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_routines(routines):
    with open(ROUTINES_FILE, "w", encoding="utf-8") as file:
        json.dump(routines, file, indent=2)


def create_routine(name, steps):
    routines = load_routines()

    routine = {
        "id": len(routines) + 1,
        "created_at": datetime.now().isoformat(),
        "name": name,
        "steps": steps,
    }

    routines.append(routine)
    save_routines(routines)

    return {
        "success": True,
        "routine": routine,
        "routine_count": len(routines),
    }


def get_routines():
    return {
        "success": True,
        "routines": load_routines(),
    }


def delete_routine(routine_id):
    routines = load_routines()

    updated = [
        routine for routine in routines
        if routine.get("id") != routine_id
    ]

    save_routines(updated)

    return {
        "success": True,
        "deleted": len(updated) != len(routines),
        "routine_id": routine_id,
    }


def format_routine_created(result):
    if not result.get("success"):
        return (
            "ROUTINE CREATE FAILED\n\n"
            f"{result.get('error')}"
        )

    routine = result.get("routine", {})

    lines = [
        "ROUTINE CREATED",
        "",
        f"ID: {routine.get('id')}",
        f"Name: {routine.get('name')}",
        f"Created: {routine.get('created_at')}",
        "",
        "Steps:",
    ]

    for step in routine.get("steps", []):
        lines.append(f"- {step}")

    return "\n".join(lines)


def format_routines(result):
    if not result.get("success"):
        return (
            "ROUTINES ERROR\n\n"
            f"{result.get('error')}"
        )

    routines = result.get("routines", [])

    if not routines:
        return "No routines created yet."

    lines = [
        "JARVIS ROUTINES",
        "",
    ]

    for routine in routines:
        lines.append(f"{routine.get('id')}. {routine.get('name')}")
        lines.append(f"Created: {routine.get('created_at')}")
        lines.append("Steps:")

        for step in routine.get("steps", []):
            lines.append(f"   - {step}")

        lines.append("")

    return "\n".join(lines)