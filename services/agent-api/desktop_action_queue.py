import json
import os
from datetime import datetime

from desktop_action_safety import validate_desktop_action

QUEUE_FILE = "desktop_action_queue.json"


def load_action_queue():
    if not os.path.exists(QUEUE_FILE):
        return []

    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_action_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as file:
        json.dump(queue, file, indent=2)


def add_desktop_action(action):
    safety = validate_desktop_action(action)

    if not safety.get("valid"):
        return {
            "success": False,
            "error": safety.get("error"),
            "safety": safety,
        }

    queue = load_action_queue()

    next_id = 1
    if queue:
        next_id = max(item.get("id", 0) for item in queue) + 1

    item = {
        "id": next_id,
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
        "requires_confirmation": safety.get("requires_confirmation"),
        "action": safety.get("action"),
    }

    queue.append(item)
    save_action_queue(queue)

    return {
        "success": True,
        "queued_action": item,
        "queue_count": len(queue),
    }


def get_action_queue():
    return {
        "success": True,
        "queue": load_action_queue(),
    }


def get_next_pending_action():
    queue = load_action_queue()

    for item in queue:
        if item.get("status") == "pending":
            return {
                "success": True,
                "queued_action": item,
                "queue": queue,
            }

    return {
        "success": False,
        "error": "No pending desktop action found.",
        "queue": queue,
    }


def mark_action_complete(action_id, success=True, message=None):
    queue = load_action_queue()
    updated_item = None

    for item in queue:
        if item.get("id") == action_id:
            item["status"] = "complete" if success else "failed"
            item["completed_at"] = datetime.now().isoformat()
            item["result_message"] = message
            updated_item = item
            break

    save_action_queue(queue)

    return {
        "success": updated_item is not None,
        "updated_action": updated_item,
        "queue": queue,
    }


def clear_action_queue():
    save_action_queue([])

    return {
        "success": True,
        "message": "Desktop action queue cleared.",
    }


def format_action_queue(result):
    if not result.get("success"):
        return f"DESKTOP ACTION QUEUE ERROR\n\n{result.get('error')}"

    queue = result.get("queue", [])

    if not queue:
        return "Desktop action queue is empty."

    lines = ["DESKTOP ACTION QUEUE", ""]

    for item in queue:
        lines.append(f"ID: {item.get('id')}")
        lines.append(f"Status: {item.get('status')}")
        lines.append(f"Requires confirmation: {item.get('requires_confirmation')}")
        lines.append(f"Action: {item.get('action')}")
        lines.append("")

    return "\n".join(lines)


def format_action_added(result):
    if not result.get("success"):
        return (
            "DESKTOP ACTION NOT QUEUED\n\n"
            f"Reason: {result.get('error')}"
        )

    return (
        "DESKTOP ACTION QUEUED\n\n"
        f"Queue count: {result.get('queue_count')}\n\n"
        f"Action: {result.get('queued_action')}"
    )