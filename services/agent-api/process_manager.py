import os
import socket
import subprocess
from datetime import datetime

try:
    import psutil
except Exception:
    psutil = None

BACKEND_PORT = 8000
FRONTEND_PORT = 5173
OLLAMA_PORT = 11434


def is_port_open(host="127.0.0.1", port=8000, timeout=1):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def get_processes_by_name(name):
    if psutil is None:
        return []

    matches = []

    for process in psutil.process_iter(["pid", "name", "cmdline", "status"]):
        try:
            proc_name = process.info.get("name") or ""
            cmdline = " ".join(process.info.get("cmdline") or [])

            if name.lower() in proc_name.lower() or name.lower() in cmdline.lower():
                matches.append({
                    "pid": process.info.get("pid"),
                    "name": proc_name,
                    "cmdline": cmdline[:500],
                    "status": process.info.get("status"),
                })
        except Exception:
            continue

    return matches


def get_service_status():
    return {
        "timestamp": datetime.now().isoformat(),
        "backend": {
            "port": BACKEND_PORT,
            "online": is_port_open(port=BACKEND_PORT),
        },
        "frontend": {
            "port": FRONTEND_PORT,
            "online": is_port_open(port=FRONTEND_PORT),
        },
        "ollama": {
            "port": OLLAMA_PORT,
            "online": is_port_open(port=OLLAMA_PORT),
            "processes": get_processes_by_name("ollama"),
        },
        "node_processes": get_processes_by_name("node"),
        "python_processes": get_processes_by_name("python"),
        "psutil_available": psutil is not None,
    }


def start_process(command, cwd=None, hidden=True):
    creationflags = 0

    if os.name == "nt" and hidden:
        creationflags = subprocess.CREATE_NO_WINDOW

    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )

        return {
            "success": True,
            "pid": process.pid,
            "command": command,
            "cwd": cwd,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": command,
            "cwd": cwd,
        }


def start_ollama():
    if is_port_open(port=OLLAMA_PORT):
        return {
            "success": True,
            "message": "Ollama is already online.",
            "command": "ollama serve",
        }

    return start_process("ollama serve", hidden=True)


def format_service_status(status):
    lines = [
        "JARVIS PRODUCTION SERVICE STATUS",
        "",
        f"Timestamp: {status.get('timestamp')}",
        "",
        f"Backend online: {status['backend']['online']} | Port: {status['backend']['port']}",
        f"Frontend online: {status['frontend']['online']} | Port: {status['frontend']['port']}",
        f"Ollama online: {status['ollama']['online']} | Port: {status['ollama']['port']}",
        "",
        f"Ollama processes: {len(status.get('ollama', {}).get('processes', []))}",
        f"Node processes: {len(status.get('node_processes', []))}",
        f"Python processes: {len(status.get('python_processes', []))}",
        f"psutil available: {status.get('psutil_available')}",
    ]

    return "\n".join(lines)


def format_start_result(result):
    if result.get("success"):
        return (
            "PROCESS STARTED\n\n"
            f"PID: {result.get('pid')}\n"
            f"Command: {result.get('command')}\n"
            f"CWD: {result.get('cwd')}\n"
            f"Message: {result.get('message', '')}"
        )

    return (
        "PROCESS START FAILED\n\n"
        f"Reason: {result.get('error')}\n"
        f"Command: {result.get('command')}\n"
        f"CWD: {result.get('cwd')}"
    )
