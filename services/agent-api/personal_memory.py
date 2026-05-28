import json
import os
from datetime import datetime

PERSONAL_MEMORY_FILE = "personal_memory.json"


def load_personal_memory():
    if not os.path.exists(PERSONAL_MEMORY_FILE):
        return []

    try:
        with open(PERSONAL_MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_personal_memory(memory):
    with open(PERSONAL_MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2)


def remember_personal_fact(category, fact):
    memory = load_personal_memory()

    item = {
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "fact": fact,
        "content": fact,
    }

    memory.append(item)
    save_personal_memory(memory)

    return {
        "success": True,
        "memory_item": item,
        "item": item,
        "memory_count": len(memory),
        "count": len(memory),
    }


def remember_personal_item(category, content):
    return remember_personal_fact(category, content)


def get_personal_memory(limit=50):
    memory = list(reversed(load_personal_memory()))

    return {
        "success": True,
        "memory": memory[:limit],
    }


def search_personal_memory(query):
    memory = load_personal_memory()
    results = []

    query_lower = query.lower()

    for item in memory:
        combined = (
            f"{item.get('category', '')} "
            f"{item.get('fact', '')} "
            f"{item.get('content', '')}"
        ).lower()

        if query_lower in combined:
            results.append(item)

    return {
        "success": True,
        "query": query,
        "results": results,
        "count": len(results),
    }


def summarize_personal_memory():
    memory = load_personal_memory()

    return {
        "success": True,
        "memory_count": len(memory),
        "memory": memory,
    }


def format_personal_memory_save(result):
    if not result.get("success"):
        return (
            "PERSONAL MEMORY SAVE FAILED\n\n"
            f"{result.get('error')}"
        )

    item = result.get("memory_item") or result.get("item") or {}

    content = item.get("fact") or item.get("content")

    return (
        "PERSONAL MEMORY SAVED\n\n"
        f"Category: {item.get('category')}\n"
        f"Content: {content}\n"
        f"Total Memories: {result.get('memory_count') or result.get('count')}"
    )


def format_personal_memory(result):
    memory = result.get("memory", [])

    if not memory:
        return "No personal memory stored yet."

    lines = [
        "PERSONAL MEMORY",
        "",
    ]

    for item in memory:
        content = item.get("fact") or item.get("content")

        lines.append(f"[{item.get('category')}] {content}")
        lines.append(f"Time: {item.get('timestamp')}")
        lines.append("")

    return "\n".join(lines)


def format_personal_memory_search(result):
    if not result.get("success"):
        return (
            "PERSONAL MEMORY SEARCH FAILED\n\n"
            f"{result.get('error')}"
        )

    results = result.get("results", [])

    if not results:
        return "No matching personal memories found."

    lines = [
        "PERSONAL MEMORY SEARCH",
        "",
        f"Results: {result.get('count')}",
        "",
    ]

    for item in results:
        content = item.get("fact") or item.get("content")

        lines.append(f"[{item.get('category')}]")
        lines.append(str(content))
        lines.append("")

    return "\n".join(lines)


def format_personal_memory_summary(result):
    if not result.get("success"):
        return (
            "PERSONAL MEMORY SUMMARY FAILED\n\n"
            f"{result.get('error')}"
        )

    memory = result.get("memory", [])

    if not memory:
        return "No personal memory stored yet."

    lines = [
        "PERSONAL MEMORY SUMMARY",
        "",
        f"Total Memories: {result.get('memory_count')}",
        "",
    ]

    for item in memory[-10:]:
        content = item.get("fact") or item.get("content")

        lines.append(f"[{item.get('category')}]")
        lines.append(str(content))
        lines.append("")

    return "\n".join(lines)