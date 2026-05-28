import time

import pyautogui

from desktop_action_safety import validate_desktop_action


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15


def execute_desktop_action(action):
    safety = validate_desktop_action(action)

    if not safety.get("valid"):
        return {
            "success": False,
            "error": safety.get("error"),
            "safety": safety,
        }

    safe_action = safety.get("action")
    action_type = safe_action.get("type")

    try:
        if action_type == "move_mouse":
            pyautogui.moveTo(
                int(safe_action.get("x")),
                int(safe_action.get("y")),
                duration=0.25,
            )

        elif action_type == "click":
            pyautogui.click(
                int(safe_action.get("x")),
                int(safe_action.get("y")),
            )

        elif action_type == "double_click":
            pyautogui.doubleClick(
                int(safe_action.get("x")),
                int(safe_action.get("y")),
            )

        elif action_type == "right_click":
            pyautogui.rightClick(
                int(safe_action.get("x")),
                int(safe_action.get("y")),
            )

        elif action_type == "type_text":
            text = safe_action.get("text") or ""
            pyautogui.write(text, interval=0.02)

        elif action_type == "press_key":
            key = safe_action.get("key")

            if not key:
                return {
                    "success": False,
                    "error": "press_key requires a key.",
                }

            pyautogui.press(key)

        elif action_type == "hotkey":
            keys = safe_action.get("keys")

            if not keys:
                return {
                    "success": False,
                    "error": "hotkey requires keys.",
                }

            if isinstance(keys, str):
                keys = [
                    item.strip()
                    for item in keys.split("+")
                    if item.strip()
                ]

            pyautogui.hotkey(*keys)

        elif action_type == "scroll":
            amount = safe_action.get("amount")

            if amount is None:
                amount = -500

            pyautogui.scroll(int(amount))

        elif action_type == "wait":
            seconds = safe_action.get("amount")

            if seconds is None:
                seconds = 1

            time.sleep(float(seconds))

        else:
            return {
                "success": False,
                "error": f"Unsupported action type: {action_type}",
            }

        return {
            "success": True,
            "message": "Desktop action executed.",
            "action": safe_action,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": safe_action,
        }


def format_desktop_action_execution(result):
    if not result.get("success"):
        return (
            "DESKTOP ACTION EXECUTION FAILED\n\n"
            f"Reason: {result.get('error')}\n\n"
            f"Action: {result.get('action')}"
        )

    return (
        "DESKTOP ACTION EXECUTED\n\n"
        f"{result.get('message')}\n\n"
        f"Action: {result.get('action')}"
    )