import json
import os

VISION_MEMORY_FILE = os.path.join("vision_output", "vision_memory.json")


def search_vision_memory(query, limit=10):
    query = query.strip().lower()

    if not query:
        return {
            "success": False,
            "error": "Vision memory search query cannot be empty.",
            "matches": [],
        }

    if not os.path.exists(VISION_MEMORY_FILE):
        return {
            "success": True,
            "query": query,
            "matches": [],
        }

    try:
        with open(VISION_MEMORY_FILE, "r", encoding="utf-8") as file:
            snapshots = json.load(file)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "matches": [],
        }

    matches = []

    for snapshot in reversed(snapshots):
        searchable = json.dumps(snapshot).lower()

        if query in searchable:
            matches.append(snapshot)

        if len(matches) >= limit:
            break

    return {
        "success": True,
        "query": query,
        "matches": matches,
    }


def format_vision_memory_search(result):
    if not result.get("success"):
        return f"VISION MEMORY SEARCH ERROR\n\n{result.get('error')}"

    matches = result.get("matches", [])

    lines = [
        "PHASE 9 VISION MEMORY SEARCH",
        "",
        f"Query: {result.get('query')}",
        f"Matches: {len(matches)}",
        "",
    ]

    if not matches:
        lines.append("No matching vision snapshots found.")
        return "\n".join(lines)

    for index, snapshot in enumerate(matches, start=1):
        summary = snapshot.get("summary", {})
        lines.append(f"{index}. {snapshot.get('timestamp')}")
        lines.append(f"   Active window: {summary.get('active_window')}")
        lines.append(f"   Regions: {summary.get('region_count')}")
        lines.append(f"   Text lines: {summary.get('text_line_count')}")
        lines.append(f"   Screenshot: {snapshot.get('screenshot')}")
        lines.append(f"   Annotated: {snapshot.get('annotated_screenshot')}")
        lines.append("")

    return "\n".join(lines)
