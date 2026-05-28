from datetime import datetime

from personal_memory import load_personal_memory
from routine_manager import load_routines


def generate_daily_summary():
    memory = load_personal_memory()
    routines = load_routines()

    return {
        "success": True,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "memory_count": len(memory),
        "routine_count": len(routines),
        "recent_memory": memory[-5:],
    }


def format_daily_summary(result):
    lines = [
        "JARVIS DAILY SUMMARY",
        "",
        f"Date: {result.get('date')}",
        f"Stored memories: {result.get('memory_count')}",
        f"Stored routines: {result.get('routine_count')}",
        "",
        "Recent memory:",
    ]

    for item in result.get("recent_memory", []):
        lines.append(f"- [{item['category']}] {item['content']}")

    return "\n".join(lines)
