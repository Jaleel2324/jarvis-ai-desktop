import sqlite3
import json
from datetime import datetime

DB_NAME = "jarvis_memory.db"


def init_screen_action_memory():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS screen_action_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        action_plan TEXT
    )
    """)

    conn.commit()
    conn.close()


def remember_screen_action_plan(action_plan):
    init_screen_action_memory()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO screen_action_memory (
        timestamp,
        action_plan
    )
    VALUES (?, ?)
    """, (
        datetime.now().isoformat(),
        json.dumps(action_plan),
    ))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "Screen action plan saved.",
        "action_plan": action_plan,
    }


def get_screen_action_memory(limit=10):
    init_screen_action_memory()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, action_plan
    FROM screen_action_memory
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    memories = []

    for row in rows:
        try:
            action_plan = json.loads(row[1])
        except Exception:
            action_plan = row[1]

        memories.append({
            "timestamp": row[0],
            "action_plan": action_plan,
        })

    return memories


def summarize_screen_action_memory(limit=10):
    memories = get_screen_action_memory(limit)

    return {
        "success": True,
        "memories": memories,
        "count": len(memories),
    }


def format_screen_action_memory_save(result):
    if not result.get("success"):
        return (
            "SCREEN ACTION MEMORY SAVE FAILED\n\n"
            f"{result.get('error')}"
        )

    return (
        "SCREEN ACTION MEMORY SAVED\n\n"
        f"{result.get('message')}"
    )


def format_screen_action_memory_summary(result):
    if not result.get("success"):
        return (
            "SCREEN ACTION MEMORY ERROR\n\n"
            f"{result.get('error')}"
        )

    memories = result.get("memories", [])

    if not memories:
        return "No screen action memory saved yet."

    lines = [
        "SCREEN ACTION MEMORY",
        "",
        f"Saved plans: {result.get('count')}",
        "",
    ]

    for index, memory in enumerate(memories, start=1):
        lines.append(f"{index}. {memory.get('timestamp')}")
        lines.append(str(memory.get("action_plan"))[:1500])
        lines.append("")

    return "\n".join(lines)