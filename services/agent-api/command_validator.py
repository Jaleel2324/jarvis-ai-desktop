def validate_contains(
    command: str,
    required_phrase: str,
    usage: str
):
    if required_phrase not in command.lower():
        return {
            "valid": False,
            "error": (
                "Invalid command format.\n\n"
                f"Use:\n{usage}"
            )
        }

    return {
        "valid": True
    }


def validate_not_empty(
    value: str,
    label: str
):
    if not value or not value.strip():
        return {
            "valid": False,
            "error": f"{label} cannot be empty."
        }

    return {
        "valid": True
    }


def validate_file_command_path(path: str):
    if not path or not path.strip():
        return {
            "valid": False,
            "error": "File path cannot be empty."
        }

    blocked_fragments = [
        "windows/system32",
        "windows/syswow64",
        "program files",
        "program files (x86)",
        "appdata/roaming/microsoft/windows/start menu",
        "appdata/local/microsoft",
        "windows/servicing",
        "windows/winsxs",
    ]

    normalized = (
        path
        .lower()
        .replace("\\", "/")
    )

    for fragment in blocked_fragments:
        if fragment in normalized:
            return {
                "valid": False,
                "error": "Blocked unsafe system path."
            }

    return {
        "valid": True
    }