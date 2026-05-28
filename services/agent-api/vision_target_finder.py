from vision_ui_mapper import build_ui_map


TARGET_TYPE_ALIASES = {
    "button": ["button_or_input_bar", "ui_element", "icon_or_card"],
    "input": ["button_or_input_bar"],
    "search": ["button_or_input_bar", "top_bar_or_header"],
    "sidebar": ["left_sidebar", "right_sidebar"],
    "panel": ["panel_or_content_block", "large_window_or_main_panel"],
    "window": ["large_window_or_main_panel"],
    "card": ["icon_or_card", "panel_or_content_block"],
    "icon": ["icon_or_card"],
    "header": ["top_bar_or_header"],
}


def find_visual_target(query):
    query = query.strip().lower()

    if not query:
        return {
            "success": False,
            "error": "Target query cannot be empty.",
        }

    ui = build_ui_map()

    if not ui.get("success"):
        return ui

    terms = query.replace("-", " ").replace("_", " ").split()
    regions = ui.get("ui_map", [])

    scored = []

    for region in regions:
        score = 0
        region_type = region.get("type", "")
        zone = region.get("zone", "")

        for term in terms:
            aliases = TARGET_TYPE_ALIASES.get(term, [])

            if term in region_type:
                score += 4

            if term in zone:
                score += 3

            if region_type in aliases:
                score += 5

        # Prefer larger, clear regions after type/zone matching.
        if score > 0:
            score += min(region.get("area", 0) / 50000, 3)

            scored.append({
                "score": round(score, 2),
                "region": region,
            })

    scored = sorted(scored, key=lambda item: item["score"], reverse=True)

    return {
        "success": True,
        "query": query,
        "matches": scored[:10],
        "active_window": ui.get("active_window"),
        "annotated_screenshot": ui.get("annotated_screenshot"),
    }


def format_visual_target(result):
    if not result.get("success"):
        return f"VISUAL TARGET ERROR\n\n{result.get('error')}"

    matches = result.get("matches", [])

    lines = [
        "PHASE 9 VISUAL TARGET FINDER",
        "",
        f"Query: {result.get('query')}",
        f"Active window: {result.get('active_window') or 'Unknown'}",
        f"Annotated screenshot: {result.get('annotated_screenshot')}",
        "",
    ]

    if not matches:
        lines.append("No matching visual target found.")
        return "\n".join(lines)

    lines.append("Best matches:")

    for index, match in enumerate(matches, start=1):
        region = match["region"]

        lines.append(
            f"{index}. Score {match['score']} | {region['type']} | {region['zone']} | "
            f"center=({region['center_x']}, {region['center_y']}) | "
            f"box=({region['x']}, {region['y']}, {region['width']}, {region['height']})"
        )

    lines.append("")
    lines.append("Note: This identifies targets only. It does not click or control the desktop.")

    return "\n".join(lines)
