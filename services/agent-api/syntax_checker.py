import subprocess
import os
import sys


def check_python_syntax(path: str):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "py_compile",
            path
        ],
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "output": (
            result.stdout.strip()
            or result.stderr.strip()
        )
    }


def check_typescript_syntax(path: str):
    if not os.path.exists(path):
        return {
            "success": False,
            "output": "File not found."
        }

    result = subprocess.run(
        [
            "npx",
            "tsc",
            "--noEmit",
            path
        ],
        capture_output=True,
        text=True,
        shell=True
    )

    return {
        "success": result.returncode == 0,
        "output": (
            result.stdout.strip()
            or result.stderr.strip()
        )
    }


def validate_file_syntax(path: str):
    extension = os.path.splitext(path)[1].lower()

    if extension == ".py":
        return check_python_syntax(path)

    if extension in [".ts", ".tsx"]:
        return check_typescript_syntax(path)

    return {
        "success": True,
        "output": "No syntax checker available."
    }