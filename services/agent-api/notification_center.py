import json
import os
from datetime import datetime

NOTIFICATION_FILE = "jarvis_notifications.json"


def load_notifications():
    if not os.path.exists(NOTIFICATION_FILE):
        return []

    try:
        with open(NOTIFICATION_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_notifications(notifications):
    with open(NOTIFICATION_FILE, "w", encoding="utf-8") as file:
        json.dump(notifications, file, indent=2)


def create_notification(title, message, level="info"):
    notifications = load_notifications()

    notification = {
        "id": len(notifications) + 1,
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "message": message,
        "level": level,
        "read": False,
    }

    notifications.append(notification)
    save_notifications(notifications)

    return {
        "success": True,
        "notification": notification,
        "count": len(notifications),
    }


def get_notifications():
    return {
        "success": True,
        "notifications": load_notifications(),
    }


def mark_notification_read(notification_id):
    notifications = load_notifications()

    updated = False

    for item in notifications:
        if item.get("id") == notification_id:
            item["read"] = True
            updated = True

    save_notifications(notifications)

    return {
        "success": updated,
        "notification_id": notification_id,
    }


def clear_notifications():
    save_notifications([])

    return {
        "success": True,
        "message": "Notifications cleared.",
    }


def format_notification_created(result):
    if not result.get("success"):
        return (
            "NOTIFICATION ERROR\n\n"
            f"{result.get('error')}"
        )

    notification = result.get("notification", {})

    return (
        "NOTIFICATION CREATED\n\n"
        f"Title: {notification.get('title')}\n"
        f"Message: {notification.get('message')}\n"
        f"Level: {notification.get('level')}"
    )


def format_notifications(result):
    if not result.get("success"):
        return (
            "NOTIFICATION CENTER ERROR\n\n"
            f"{result.get('error')}"
        )

    notifications = result.get("notifications", [])

    if not notifications:
        return "No notifications available."

    lines = [
        "JARVIS NOTIFICATION CENTER",
        "",
    ]

    for item in notifications:
        lines.append(
            f"[{item.get('level').upper()}] "
            f"{item.get('title')}"
        )

        lines.append(item.get("message"))
        lines.append(f"Read: {item.get('read')}")
        lines.append(f"Time: {item.get('timestamp')}")
        lines.append("")

    return "\n".join(lines)