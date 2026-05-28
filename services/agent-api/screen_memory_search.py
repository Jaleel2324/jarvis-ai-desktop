import json
import os

from screen_memory import SCREEN_MEMORY_FILE


def load_screen_memories():
    if not os.path.exists(SCREEN_MEMORY_FILE):
        return []

    with open(SCREEN_MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_screen_memory(query: str):
    memories = load_screen_memories()

    if not memories:
        return {
            "success": True,
            "results": [],
            "query": query,
        }

    query_lower = query.lower()

    matches = []

    for memory in memories:
        text = memory.get("text", "")

        if query_lower in text.lower():
            matches.append(memory)

    return {
        "success": True,
        "query": query,
        "results": matches[:10],
        "total_matches": len(matches),
    }


def format_screen_memory_search(result: dict):
    matches = result.get("results", [])

    if not matches:
        return (
            "SCREEN MEMORY SEARCH\n\n"
            f"No matches found for:\n"
            f"{result.get('query')}"
        )

    sections = []

    for index, item in enumerate(matches, start=1):
        sections.append(
            (
                f"[{index}]\n"
                f"Time: {item.get('created_at')}\n"
                f"Screenshot: {item.get('screenshot')}\n"
                f"OCR File: {item.get('ocr_file')}\n\n"
                f"Text:\n"
                f"{item.get('text', '')[:1000]}"
            )
        )

    joined = "\n\n-------------------\n\n".join(sections)

    return (
        "SCREEN MEMORY SEARCH RESULTS\n\n"
        f"Query: {result.get('query')}\n"
        f"Matches: {result.get('total_matches', 0)}\n\n"
        f"{joined}"
    )