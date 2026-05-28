import json
import os
from datetime import datetime

MEMORY_FILE = "jarvis_long_term_memory.json"


def _load_raw_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_raw_memory(items):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(items, file, indent=2)


def save_memory(category, content, source="user", importance=3):
    content = str(content).strip()
    category = str(category).strip().lower() or "general"
    source = str(source).strip().lower() or "user"

    if not content:
        return {"success": False, "error": "Memory content cannot be empty."}

    items = _load_raw_memory()

    item = {
        "id": len(items) + 1,
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "source": source,
        "importance": int(importance),
        "content": content,
    }

    items.append(item)
    items = items[-2000:]

    _save_raw_memory(items)

    return {"success": True, "memory": item, "count": len(items)}


def list_memories(limit=25):
    items = list(reversed(_load_raw_memory()))
    return {"success": True, "memories": items[:limit], "count": len(items)}


def search_memories(query, limit=15):
    query = str(query).strip().lower()

    if not query:
        return {
            "success": False,
            "error": "Search query cannot be empty.",
            "matches": [],
        }

    items = _load_raw_memory()
    matches = []

    for item in reversed(items):
        searchable = " ".join([
            str(item.get("category", "")),
            str(item.get("source", "")),
            str(item.get("content", "")),
        ]).lower()

        if query in searchable:
            matches.append(item)

        if len(matches) >= limit:
            break

    return {
        "success": True,
        "query": query,
        "matches": matches,
        "count": len(matches),
    }


def summarize_memory(limit=50):
    items = _load_raw_memory()
    recent = items[-limit:]
    categories = {}

    for item in items:
        category = item.get("category", "general")
        categories[category] = categories.get(category, 0) + 1

    return {
        "success": True,
        "total_memories": len(items),
        "categories": categories,
        "recent": list(reversed(recent)),
    }


def format_memory_saved(result):
    if not result.get("success"):
        return "MEMORY SAVE FAILED\n\n" + str(result.get("error"))

    item = result.get("memory", {})

    return (
        "MEMORY SAVED\n\n"
        f"ID: {item.get('id')}\n"
        f"Category: {item.get('category')}\n"
        f"Importance: {item.get('importance')}\n"
        f"Content: {item.get('content')}\n"
        f"Total memories: {result.get('count')}"
    )


def format_memory_list(result):
    if not result.get("success"):
        return "MEMORY LIST FAILED\n\n" + str(result.get("error"))

    memories = result.get("memories", [])

    if not memories:
        return "No memories stored yet."

    lines = ["JARVIS LONG-TERM MEMORY", "", f"Showing: {len(memories)}", ""]

    for item in memories:
        lines.append(f"{item.get('id')}. [{item.get('category')}] {item.get('content')}")
        lines.append(f"   Source: {item.get('source')} | Importance: {item.get('importance')}")
        lines.append(f"   Time: {item.get('timestamp')}")
        lines.append("")

    return "\n".join(lines)


def format_memory_search(result):
    if not result.get("success"):
        return "MEMORY SEARCH FAILED\n\n" + str(result.get("error"))

    matches = result.get("matches", [])

    if not matches:
        return f"No memory matches found for: {result.get('query')}"

    lines = [
        "JARVIS MEMORY SEARCH",
        "",
        f"Query: {result.get('query')}",
        f"Matches: {result.get('count')}",
        "",
    ]

    for item in matches:
        lines.append(f"{item.get('id')}. [{item.get('category')}] {item.get('content')}")
        lines.append(f"   Time: {item.get('timestamp')}")
        lines.append("")

    return "\n".join(lines)


def format_memory_summary(result):
    if not result.get("success"):
        return "MEMORY SUMMARY FAILED\n\n" + str(result.get("error"))

    lines = [
        "JARVIS MEMORY SUMMARY",
        "",
        f"Total memories: {result.get('total_memories')}",
        "",
        "Categories:",
    ]

    categories = result.get("categories", {})

    if not categories:
        lines.append("- None yet")
    else:
        for category, count in categories.items():
            lines.append(f"- {category}: {count}")

    recent = result.get("recent", [])

    lines.extend(["", "Recent memories:"])

    if not recent:
        lines.append("- None yet")
    else:
        for item in recent[:10]:
            lines.append(f"- [{item.get('category')}] {item.get('content')}")

    return "\n".join(lines)
