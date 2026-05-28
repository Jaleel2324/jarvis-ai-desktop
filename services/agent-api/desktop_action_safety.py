DANGEROUS_KEYWORDS = [
    "delete",
    "remove",
    "format",
    "shutdown",
    "restart",
    "wipe",
    "erase",
    "uninstall",
    "factory reset",
    "registry",
    "regedit",
    "powershell admin",
    "administrator",
    "cmd admin",
    "taskkill",
    "kill process",
    "close all",
    "empty recycle bin",
    "diskpart",
    "partition",
    "encrypt",
    "decrypt",
    "password",
    "bank",
    "payment",
    "checkout",
    "purchase",
    "send money",
    "transfer money",
    "submit application",
    "sign document",
    "upload id",
    "social security",
    "ssn",
]

ALLOWED_ACTION_TYPES = [
    "move_mouse",
    "click",
    "double_click",
    "right_click",
    "type_text",
    "press_key",
    "hotkey",
    "scroll",
    "wait",
]


REQUIRES_CONFIRMATION = [
    "click",
    "double_click",
    "right_click",
    "type_text",
    "press_key",
    "hotkey",
    "scroll",
]


def normalize_action(action):
    if not isinstance(action, dict):
        return {
            "valid": False,
            "error": "Desktop action must be a dictionary.",
            "action": None,
        }

    action_type = str(action.get("type", "")).strip().lower()

    normalized = {
        "type": action_type,
        "x": action.get("x"),
        "y": action.get("y"),
        "text": action.get("text"),
        "key": action.get("key"),
        "keys": action.get("keys"),
        "amount": action.get("amount"),
        "reason": action.get("reason", ""),
    }

    return {
        "valid": True,
        "action": normalized,
    }


def action_contains_dangerous_content(action):
    combined = " ".join([
        str(action.get("type", "")),
        str(action.get("text", "")),
        str(action.get("key", "")),
        str(action.get("keys", "")),
        str(action.get("reason", "")),
    ]).lower()

    for keyword in DANGEROUS_KEYWORDS:
        if keyword in combined:
            return True, keyword

    return False, None


def validate_coordinates(action):
    action_type = action.get("type")

    if action_type not in [
        "move_mouse",
        "click",
        "double_click",
        "right_click",
    ]:
        return {
            "valid": True,
        }

    x = action.get("x")
    y = action.get("y")

    if x is None or y is None:
        return {
            "valid": False,
            "error": "Mouse action requires x and y coordinates.",
        }

    try:
        x = int(x)
        y = int(y)
    except Exception:
        return {
            "valid": False,
            "error": "Mouse coordinates must be numbers.",
        }

    if x < 0 or y < 0:
        return {
            "valid": False,
            "error": "Mouse coordinates cannot be negative.",
        }

    return {
        "valid": True,
    }


def validate_desktop_action(action):
    normalized_result = normalize_action(action)

    if not normalized_result["valid"]:
        return normalized_result

    normalized = normalized_result["action"]
    action_type = normalized.get("type")

    if action_type not in ALLOWED_ACTION_TYPES:
        return {
            "valid": False,
            "requires_confirmation": False,
            "blocked": True,
            "error": f"Desktop action type not allowed: {action_type}",
            "action": normalized,
        }

    coordinate_check = validate_coordinates(normalized)

    if not coordinate_check["valid"]:
        return {
            "valid": False,
            "requires_confirmation": False,
            "blocked": True,
            "error": coordinate_check["error"],
            "action": normalized,
        }

    dangerous, keyword = action_contains_dangerous_content(normalized)

    if dangerous:
        return {
            "valid": False,
            "requires_confirmation": False,
            "blocked": True,
            "error": f"Action blocked because it contains risky keyword: {keyword}",
            "action": normalized,
        }

    return {
        "valid": True,
        "requires_confirmation": action_type in REQUIRES_CONFIRMATION,
        "blocked": False,
        "error": None,
        "action": normalized,
    }


def format_action_safety_result(result):
    action = result.get("action")

    if result.get("blocked"):
        return (
            "DESKTOP ACTION BLOCKED\n\n"
            f"Reason: {result.get('error')}\n\n"
            f"Action: {action}"
        )

    if not result.get("valid"):
        return (
            "DESKTOP ACTION INVALID\n\n"
            f"Reason: {result.get('error')}\n\n"
            f"Action: {action}"
        )

    confirmation_text = (
        "Yes" if result.get("requires_confirmation") else "No"
    )

    return (
        "DESKTOP ACTION SAFETY CHECK PASSED\n\n"
        f"Requires confirmation: {confirmation_text}\n\n"
        f"Action: {action}"
    )