import os
import json
from datetime import datetime

import cv2
import numpy as np
from PIL import Image, ImageGrab

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pygetwindow as gw
except Exception:
    gw = None


SCREENSHOT_DIR = "screenshots"
VISION_DIR = "vision_output"
VISION_MEMORY_FILE = os.path.join(VISION_DIR, "vision_memory.json")


def ensure_dirs():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(VISION_DIR, exist_ok=True)


def capture_live_screen_for_vision():
    ensure_dirs()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_DIR, f"vision_capture_{timestamp}.png")

    image = ImageGrab.grab()
    image.save(path)

    return path


def get_latest_screenshot_path():
    ensure_dirs()

    files = [
        os.path.join(SCREENSHOT_DIR, file)
        for file in os.listdir(SCREENSHOT_DIR)
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not files:
        return capture_live_screen_for_vision()

    return max(files, key=os.path.getmtime)


def get_cursor_position():
    if pyautogui is None:
        return {
            "available": False,
            "x": None,
            "y": None,
        }

    try:
        x, y = pyautogui.position()
        return {
            "available": True,
            "x": int(x),
            "y": int(y),
        }
    except Exception:
        return {
            "available": False,
            "x": None,
            "y": None,
        }


def get_window_snapshot():
    if gw is None:
        return {
            "available": False,
            "active_window": None,
            "windows": [],
            "note": "Install pygetwindow for window awareness.",
        }

    try:
        active = gw.getActiveWindow()
        windows = []

        for window in gw.getAllWindows():
            title = (window.title or "").strip()

            if not title:
                continue

            windows.append({
                "title": title,
                "x": int(window.left),
                "y": int(window.top),
                "width": int(window.width),
                "height": int(window.height),
                "is_active": active is not None and title == active.title,
            })

        active_window = None

        if active is not None:
            active_window = {
                "title": active.title,
                "x": int(active.left),
                "y": int(active.top),
                "width": int(active.width),
                "height": int(active.height),
            }

        return {
            "available": True,
            "active_window": active_window,
            "windows": windows[:25],
        }

    except Exception as e:
        return {
            "available": False,
            "active_window": None,
            "windows": [],
            "error": str(e),
        }


def classify_region(x, y, w, h, screen_width, screen_height):
    area = w * h
    screen_area = screen_width * screen_height
    aspect = w / max(h, 1)

    if area > screen_area * 0.45:
        return "large_window_or_main_panel"

    if y < screen_height * 0.15 and w > screen_width * 0.25:
        return "top_bar_or_header"

    if x < screen_width * 0.18 and h > screen_height * 0.25:
        return "left_sidebar"

    if x > screen_width * 0.75 and h > screen_height * 0.25:
        return "right_sidebar"

    if h < 80 and w > 140:
        return "button_or_input_bar"

    if 0.7 <= aspect <= 1.4 and 40 <= w <= 180 and 40 <= h <= 180:
        return "icon_or_card"

    if area > 25000:
        return "panel_or_content_block"

    return "ui_element"


def detect_visual_regions(image):
    height, width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 60, 150)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        closed,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    regions = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h

        if area < 1200:
            continue

        if w < 25 or h < 20:
            continue

        region_type = classify_region(x, y, w, h, width, height)

        regions.append({
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h),
            "area": int(area),
            "type": region_type,
        })

    regions = sorted(
        regions,
        key=lambda item: item["area"],
        reverse=True,
    )

    return regions[:40]


def detect_text_like_lines(image):
    height, width = image.shape[:2]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        10,
    )

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 2))
    detected_lines = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        horizontal_kernel,
        iterations=1,
    )

    contours, _ = cv2.findContours(
        detected_lines,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    lines = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if w > 60 and 3 <= h <= 35:
            lines.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h),
            })

    lines = sorted(lines, key=lambda item: (item["y"], item["x"]))

    return lines[:80]


def create_annotated_image(path, regions, cursor):
    image = cv2.imread(path)

    if image is None:
        return None

    for index, region in enumerate(regions[:25], start=1):
        x = region["x"]
        y = region["y"]
        w = region["width"]
        h = region["height"]

        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            image,
            str(index),
            (x, max(y - 6, 15)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    if cursor.get("available"):
        cx = cursor["x"]
        cy = cursor["y"]

        cv2.circle(image, (cx, cy), 12, (0, 0, 255), 2)
        cv2.line(image, (cx - 18, cy), (cx + 18, cy), (0, 0, 255), 2)
        cv2.line(image, (cx, cy - 18), (cx, cy + 18), (0, 0, 255), 2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(VISION_DIR, f"annotated_vision_{timestamp}.png")

    cv2.imwrite(output_path, image)

    return output_path


def analyze_screen_vision():
    ensure_dirs()

    path = get_latest_screenshot_path()
    image = cv2.imread(path)

    if image is None:
        return {
            "success": False,
            "error": f"Could not read screenshot: {path}",
        }

    height, width = image.shape[:2]

    regions = detect_visual_regions(image)
    text_lines = detect_text_like_lines(image)
    cursor = get_cursor_position()
    windows = get_window_snapshot()
    annotated_path = create_annotated_image(path, regions, cursor)

    result = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "screenshot": path,
        "annotated_screenshot": annotated_path,
        "screen_size": {
            "width": int(width),
            "height": int(height),
        },
        "cursor": cursor,
        "windows": windows,
        "visual_regions": regions,
        "text_like_lines": text_lines,
        "summary": {
            "region_count": len(regions),
            "text_line_count": len(text_lines),
            "active_window": (
                windows.get("active_window", {}).get("title")
                if windows.get("active_window")
                else None
            ),
        },
    }

    return result


def remember_vision_snapshot(result):
    ensure_dirs()

    existing = []

    if os.path.exists(VISION_MEMORY_FILE):
        try:
            with open(VISION_MEMORY_FILE, "r", encoding="utf-8") as file:
                existing = json.load(file)
        except Exception:
            existing = []

    existing.append(result)
    existing = existing[-100:]

    with open(VISION_MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(existing, file, indent=2)

    return {
        "success": True,
        "message": "Vision snapshot remembered.",
        "total_snapshots": len(existing),
    }


def load_vision_memory(limit=10):
    ensure_dirs()

    if not os.path.exists(VISION_MEMORY_FILE):
        return {
            "success": True,
            "snapshots": [],
        }

    try:
        with open(VISION_MEMORY_FILE, "r", encoding="utf-8") as file:
            snapshots = json.load(file)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "snapshots": [],
        }

    return {
        "success": True,
        "snapshots": snapshots[-limit:],
    }


def format_vision_result(result):
    if not result.get("success"):
        return f"PHASE 9 VISION ERROR\n\n{result.get('error')}"

    active_window = result.get("summary", {}).get("active_window") or "Unknown"

    lines = [
        "PHASE 9 REAL VISION ONLINE",
        "",
        f"Screenshot: {result.get('screenshot')}",
        f"Annotated screenshot: {result.get('annotated_screenshot')}",
        f"Screen size: {result['screen_size']['width']} x {result['screen_size']['height']}",
        f"Active window: {active_window}",
        f"Cursor: {result.get('cursor')}",
        "",
        f"Detected visual regions: {result['summary']['region_count']}",
        f"Detected text-like lines: {result['summary']['text_line_count']}",
        "",
        "Top visual regions:",
    ]

    for index, region in enumerate(result.get("visual_regions", [])[:12], start=1):
        lines.append(
            f"{index}. {region['type']} "
            f"x={region['x']} y={region['y']} "
            f"w={region['width']} h={region['height']}"
        )

    windows = result.get("windows", {}).get("windows", [])

    if windows:
        lines.append("")
        lines.append("Visible windows:")

        for window in windows[:8]:
            marker = "*" if window.get("is_active") else "-"
            lines.append(
                f"{marker} {window.get('title')} "
                f"({window.get('width')}x{window.get('height')})"
            )

    return "\n".join(lines)


def format_vision_memory(result):
    if not result.get("success"):
        return f"VISION MEMORY ERROR\n\n{result.get('error')}"

    snapshots = result.get("snapshots", [])

    if not snapshots:
        return "No vision snapshots stored yet."

    lines = [
        "PHASE 9 VISION MEMORY",
        "",
        f"Snapshots shown: {len(snapshots)}",
        "",
    ]

    for index, snapshot in enumerate(reversed(snapshots), start=1):
        summary = snapshot.get("summary", {})
        lines.append(f"{index}. {snapshot.get('timestamp')}")
        lines.append(f"   Active window: {summary.get('active_window')}")
        lines.append(f"   Regions: {summary.get('region_count')}")
        lines.append(f"   Text lines: {summary.get('text_line_count')}")
        lines.append(f"   Annotated: {snapshot.get('annotated_screenshot')}")
        lines.append("")

    return "\n".join(lines)
