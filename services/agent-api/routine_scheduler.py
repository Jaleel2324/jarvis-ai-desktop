import json
import os
from datetime import datetime

SCHEDULE_FILE = "jarvis_routine_schedule.json"


def load_routine_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return []

    try:
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_routine_schedule(schedule):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as file:
        json.dump(schedule, file, indent=2)


def schedule_routine(name, time_of_day):
    schedule = load_routine_schedule()

    item = {
        "id": len(schedule) + 1,
        "routine": name,
        "scheduled_for": time_of_day,
        "created_at": datetime.now().isoformat(),
    }

    schedule.append(item)
    save_routine_schedule(schedule)

    return {
        "success": True,
        "schedule": item,
    }


def get_routine_schedule():
    return {
        "success": True,
        "schedule": load_routine_schedule(),
    }


def clear_routine_schedule():
    save_routine_schedule([])

    return {
        "success": True,
        "message": "Routine schedule cleared.",
    }


def format_schedule_result(result):
    if not result.get("success"):
        return (
            "ROUTINE SCHEDULE FAILED\n\n"
            f"{result.get('error')}"
        )

    item = result.get("schedule", {})

    return (
        "ROUTINE SCHEDULED\n\n"
        f"Routine: {item.get('routine')}\n"
        f"Time: {item.get('scheduled_for')}\n"
        f"Created: {item.get('created_at')}"
    )


def format_routine_schedule(result):
    if not result.get("success"):
        return (
            "ROUTINE SCHEDULE ERROR\n\n"
            f"{result.get('error')}"
        )

    schedule = result.get("schedule", [])

    if not schedule:
        return "No scheduled routines."

    lines = [
        "JARVIS ROUTINE SCHEDULE",
        "",
    ]

    for item in schedule:
        lines.append(
            f"{item.get('id')}. {item.get('routine')} "
            f"at {item.get('scheduled_for')}"
        )

    return "\n".join(lines)