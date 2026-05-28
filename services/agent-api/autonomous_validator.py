import os
import subprocess


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)


FRONTEND_PATH = os.path.join(
    PROJECT_ROOT,
    "apps",
    "desktop",
)


def run_command(command: str, cwd: str):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        return {
            "success": result.returncode == 0,
            "command": command,
            "cwd": cwd,
            "return_code": result.returncode,
            "output": output[:4000],
            "error": error[:4000],
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "command": command,
            "cwd": cwd,
            "return_code": -1,
            "output": "",
            "error": "Validation timed out.",
        }

    except Exception as e:
        return {
            "success": False,
            "command": command,
            "cwd": cwd,
            "return_code": -1,
            "output": "",
            "error": str(e),
        }


def validate_python_file(path: str):
    if not os.path.exists(path):
        return {
            "success": False,
            "error": f"File not found: {path}",
        }

    return run_command(
        f'python -m py_compile "{path}"',
        os.path.dirname(path),
    )


def validate_backend():
    return run_command(
        "python -m py_compile main.py",
        os.path.dirname(__file__),
    )


def validate_frontend_build():
    if not os.path.exists(FRONTEND_PATH):
        return {
            "success": False,
            "command": "npm run build",
            "cwd": FRONTEND_PATH,
            "return_code": -1,
            "output": "",
            "error": f"Frontend path not found: {FRONTEND_PATH}",
        }

    return run_command(
        "npm run build",
        FRONTEND_PATH,
    )


def run_autonomous_validation():
    backend_result = validate_backend()
    frontend_result = validate_frontend_build()

    success = (
        backend_result.get("success") and
        frontend_result.get("success")
    )

    return {
        "success": success,
        "backend": backend_result,
        "frontend": frontend_result,
    }


def format_validation_result(result: dict):
    backend = result.get("backend", {})
    frontend = result.get("frontend", {})

    backend_status = "PASSED" if backend.get("success") else "FAILED"
    frontend_status = "PASSED" if frontend.get("success") else "FAILED"

    return (
        "JARVIS AUTONOMOUS VALIDATION\n\n"
        f"Overall: {'PASSED' if result.get('success') else 'FAILED'}\n\n"
        "Backend Validation:\n"
        f"- Status: {backend_status}\n"
        f"- Command: {backend.get('command')}\n"
        f"- Error: {backend.get('error') or 'None'}\n\n"
        "Frontend Validation:\n"
        f"- Status: {frontend_status}\n"
        f"- Command: {frontend.get('command')}\n"
        f"- Error: {frontend.get('error') or 'None'}\n\n"
        "Backend Output:\n"
        f"{backend.get('output') or 'No output'}\n\n"
        "Frontend Output:\n"
        f"{frontend.get('output') or 'No output'}"
    )