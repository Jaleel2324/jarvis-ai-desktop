from vision_system import analyze_screen_vision


def build_ui_map():
    vision = analyze_screen_vision()

    if not vision.get("success"):
        return {
            "success": False,
            "error": vision.get("error"),
        }

    regions = vision.get("visual_regions", [])
    screen = vision.get("screen_size", {})
    width = screen.get("width", 1)
    height = screen.get("height", 1)

    mapped = []

    for index, region in enumerate(regions, start=1):
        x = region["x"]
        y = region["y"]
        w = region["width"]
        h = region["height"]

        center_x = x + (w // 2)
        center_y = y + (h // 2)

        if y < height * 0.2:
            vertical_zone = "top"
        elif y > height * 0.75:
            vertical_zone = "bottom"
        else:
            vertical_zone = "middle"

        if x < width * 0.25:
            horizontal_zone = "left"
        elif x > width * 0.70:
            horizontal_zone = "right"
        else:
            horizontal_zone = "center"

        mapped.append({
            "id": index,
            "type": region.get("type", "ui_element"),
            "zone": f"{vertical_zone}-{horizontal_zone}",
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "center_x": center_x,
            "center_y": center_y,
            "area": region.get("area", w * h),
        })

    return {
        "success": True,
        "screenshot": vision.get("screenshot"),
        "annotated_screenshot": vision.get("annotated_screenshot"),
        "screen_size": screen,
        "active_window": vision.get("summary", {}).get("active_window"),
        "ui_map": mapped,
        "count": len(mapped),
    }


def format_ui_map(result):
    if not result.get("success"):
        return f"UI MAP ERROR\n\n{result.get('error')}"

    lines = [
        "PHASE 9 UI MAP",
        "",
        f"Active window: {result.get('active_window') or 'Unknown'}",
        f"Screenshot: {result.get('screenshot')}",
        f"Annotated: {result.get('annotated_screenshot')}",
        f"Mapped regions: {result.get('count')}",
        "",
    ]

    if not result.get("ui_map"):
        lines.append("No UI regions mapped.")
        return "\n".join(lines)

    lines.append("Mapped UI regions:")

    for item in result.get("ui_map", [])[:25]:
        lines.append(
            f"{item['id']}. {item['type']} | {item['zone']} | "
            f"center=({item['center_x']}, {item['center_y']}) | "
            f"box=({item['x']}, {item['y']}, {item['width']}, {item['height']})"
        )

    return "\n".join(lines)
