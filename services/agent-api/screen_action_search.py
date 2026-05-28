import sqlite3
import json

DB_NAME = "jarvis_memory.db"


def search_screen_action_memory(query, limit=10):
    query = query.strip().lower()

    if not query:
        return {
            "success": False,
            "error": "Search query cannot be empty.",
            "matches": [],
        }

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, screen_context, action_plan
    FROM screen_action_memory
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    matches = []

    for row in rows:
        timestamp = row[0]
        screen_context = row[1] or ""
        action_plan_raw = row[2] or ""

        searchable_text = f"{screen_context} {action_plan_raw}".lower()

        if query in searchable_text:
            try:
                action_plan = json.loads(action_plan_raw)
            except Exception:
                action_plan = action_plan_raw

            matches.append({
                "timestamp": timestamp,
                "screen_context": screen_context,
                "action_plan": action_plan,
            })

        if len(matches) >= limit:
            break

    return {
        "success": True,
        "query": query,
        "matches": matches,
    }


def format_screen_action_search(result):
    if not result.get("success"):
        return f"Screen action search failed:\n{result.get('error')}"

    matches = result.get("matches", [])

    if not matches:
        return (
            "No matching screen action memories found.\n\n"
            f"Query: {result.get('query')}"
        )

    lines = [
        "SCREEN ACTION MEMORY SEARCH",
        "",
        f"Query: {result.get('query')}",
        f"Matches: {len(matches)}",
        "",
    ]

    for index, match in enumerate(matches, start=1):
        lines.append(f"--- Match {index} ---")
        lines.append(f"Time: {match.get('timestamp')}")
        lines.append("")
        lines.append("Screen Context:")
        lines.append(str(match.get("screen_context"))[:1000])
        lines.append("")
        lines.append("Action Plan:")
        lines.append(str(match.get("action_plan"))[:1500])
        lines.append("")

    return "\n".join(lines)