import json


def parse_desktop_action_from_text(command):
    """
    Accepts commands like:

    queue desktop action {"type":"move_mouse","x":100,"y":200}
    queue click 100 200
    queue move mouse 100 200
    queue type hello world
    queue press enter
    queue hotkey ctrl+s
    queue scroll -500
    queue wait 2
    """

    raw = command.strip()
    lower = raw.lower()

    prefixes = [
        "queue desktop action ",
        "test desktop action ",
    ]

    for prefix in prefixes:
        if lower.startswith(prefix):
            raw = raw[len(prefix):].strip()
            lower = raw.lower()
            break

    if raw.startswith("{"):
        return json.loads(raw)

    if lower.startswith("click "):
        parts = raw.split()
        return {
            "type": "click",
            "x": int(parts[1]),
            "y": int(parts[2]),
            "reason": "Queued click from command.",
        }

    if lower.startswith("double click "):
        parts = raw.split()
        return {
            "type": "double_click",
            "x": int(parts[2]),
            "y": int(parts[3]),
            "reason": "Queued double click from command.",
        }

    if lower.startswith("right click "):
        parts = raw.split()
        return {
            "type": "right_click",
            "x": int(parts[2]),
            "y": int(parts[3]),
            "reason": "Queued right click from command.",
        }

    if lower.startswith("move mouse "):
        parts = raw.split()
        return {
            "type": "move_mouse",
            "x": int(parts[2]),
            "y": int(parts[3]),
            "reason": "Queued mouse movement from command.",
        }

    if lower.startswith("type "):
        text = raw.replace("type ", "", 1)
        return {
            "type": "type_text",
            "text": text,
            "reason": "Queued typing from command.",
        }

    if lower.startswith("press "):
        key = raw.replace("press ", "", 1).strip()
        return {
            "type": "press_key",
            "key": key,
            "reason": "Queued key press from command.",
        }

    if lower.startswith("hotkey "):
        keys = raw.replace("hotkey ", "", 1).strip()
        return {
            "type": "hotkey",
            "keys": keys,
            "reason": "Queued hotkey from command.",
        }

    if lower.startswith("scroll "):
        amount = raw.replace("scroll ", "", 1).strip()
        return {
            "type": "scroll",
            "amount": int(amount),
            "reason": "Queued scroll from command.",
        }

    if lower.startswith("wait "):
        amount = raw.replace("wait ", "", 1).strip()
        return {
            "type": "wait",
            "amount": float(amount),
            "reason": "Queued wait from command.",
        }

    raise ValueError(
        "Could not parse desktop action. Use JSON or commands like: "
        "queue click 100 200, queue type hello, queue hotkey ctrl+s"
    )
