from memory_core import search_memories, summarize_memory
from conversation_memory import get_recent_conversation


def build_memory_context(user_message, max_memories=5):
    memory_matches = search_memories(user_message, limit=max_memories)
    recent_conversation = get_recent_conversation(limit=5)
    summary = summarize_memory(limit=20)

    lines = [
        "JARVIS MEMORY CONTEXT",
        "",
        f"Total stored memories: {summary.get('total_memories', 0)}",
        "",
        "Relevant memories:",
    ]

    matches = memory_matches.get("matches", [])

    if not matches:
        lines.append("- None found")
    else:
        for item in matches:
            lines.append(f"- [{item.get('category')}] {item.get('content')}")

    lines.extend(["", "Recent conversation:"])

    exchanges = recent_conversation.get("exchanges", [])

    if not exchanges:
        lines.append("- None yet")
    else:
        for exchange in reversed(exchanges):
            lines.append(f"User: {exchange.get('user')}")
            lines.append(f"JARVIS: {exchange.get('jarvis')}")

    return {
        "success": True,
        "context": "\n".join(lines),
        "memory_matches": matches,
        "recent_conversation": exchanges,
    }


def format_memory_context(result):
    if not result.get("success"):
        return "MEMORY CONTEXT FAILED\n\n" + str(result.get("error"))

    return result.get("context", "")
