import json
import os
from datetime import datetime

CONVERSATION_MEMORY_FILE = "jarvis_conversation_memory.json"


def _load_conversations():
    if not os.path.exists(CONVERSATION_MEMORY_FILE):
        return []

    try:
        with open(CONVERSATION_MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except Exception:
        return []


def _save_conversations(items):
    with open(CONVERSATION_MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(items, file, indent=2)


def remember_exchange(user_text, jarvis_text):
    user_text = str(user_text).strip()
    jarvis_text = str(jarvis_text).strip()

    user_text = user_text[:4000]
    jarvis_text = jarvis_text[:4000]

    if not user_text and not jarvis_text:
        return {
            "success": False,
            "error": "Conversation exchange is empty.",
        }

    items = _load_conversations()

    item = {
        "id": len(items) + 1,
        "timestamp": datetime.now().isoformat(),
        "user": user_text,
        "jarvis": jarvis_text,
    }

    items.append(item)
    items = items[-1000:]

    _save_conversations(items)

    return {
        "success": True,
        "exchange": item,
        "count": len(items),
    }


def get_recent_conversation(limit=10):
    items = list(reversed(_load_conversations()))

    return {
        "success": True,
        "exchanges": items[:limit],
        "count": len(items),
    }


def search_conversation(query, limit=10):
    query = str(query).strip().lower()

    if not query:
        return {
            "success": False,
            "error": "Conversation search query cannot be empty.",
            "matches": [],
        }

    items = _load_conversations()
    matches = []

    for item in reversed(items):
        combined = f"{item.get('user', '')} {item.get('jarvis', '')}".lower()

        if query in combined:
            matches.append(item)

        if len(matches) >= limit:
            break

    return {
        "success": True,
        "query": query,
        "matches": matches,
        "count": len(matches),
    }


def format_recent_conversation(result):
    if not result.get("success"):
        return (
            "CONVERSATION MEMORY FAILED\n\n"
            f"{result.get('error')}"
        )

    exchanges = result.get("exchanges", [])

    if not exchanges:
        return "No conversation memory stored yet."

    lines = [
        "RECENT CONVERSATION MEMORY",
        "",
    ]

    for item in exchanges:
        lines.append(f"{item.get('id')}. {item.get('timestamp')}")
        lines.append(f"User: {item.get('user')}")
        lines.append(f"JARVIS: {item.get('jarvis')}")
        lines.append("")

    return "\n".join(lines)


def format_conversation_search(result):
    if not result.get("success"):
        return (
            "CONVERSATION SEARCH FAILED\n\n"
            f"{result.get('error')}"
        )

    matches = result.get("matches", [])

    if not matches:
        return f"No conversation matches found for: {result.get('query')}"

    lines = [
        "CONVERSATION MEMORY SEARCH",
        "",
        f"Query: {result.get('query')}",
        f"Matches: {result.get('count')}",
        "",
    ]

    for item in matches:
        lines.append(f"{item.get('id')}. {item.get('timestamp')}")
        lines.append(f"User: {item.get('user')}")
        lines.append(f"JARVIS: {item.get('jarvis')}")
        lines.append("")

    return "\n".join(lines)