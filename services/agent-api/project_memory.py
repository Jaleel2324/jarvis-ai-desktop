import json
import os
from datetime import datetime
from project_analyzer import analyze_project


MEMORY_DIR = os.path.expanduser(
    "~/OneDrive/Desktop/jarvis-os/memory"
)

MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "project_memory.json"
)


def ensure_memory_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)


def load_memory():
    ensure_memory_dir()

    if not os.path.exists(MEMORY_FILE):
        return {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "project_summary": {},
            "frontend": {},
            "backend": {},
            "architecture_notes": [],
            "important_files": [],
            "systems": [],
        }

    try:
        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception:
        return {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "project_summary": {},
            "frontend": {},
            "backend": {},
            "architecture_notes": [],
            "important_files": [],
            "systems": [],
        }


def save_memory(memory: dict):
    ensure_memory_dir()

    memory["updated_at"] = datetime.now().isoformat()

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            memory,
            file,
            indent=2
        )


def rebuild_project_memory():
    analysis = analyze_project()

    memory = load_memory()

    memory["project_summary"] = {
        "total_files": analysis["total_files"],
        "frontend_count": len(
            analysis["frontend_files"]
        ),
        "backend_count": len(
            analysis["backend_files"]
        ),
        "other_count": len(
            analysis["other_files"]
        ),
    }

    memory["frontend"] = {
        "files": analysis["frontend_files"]
    }

    memory["backend"] = {
        "files": analysis["backend_files"]
    }

    important_files = []

    for file in analysis["frontend_files"]:
        lower = file.lower()

        if (
            "app.tsx" in lower
            or "orb.ts" in lower
            or "voice" in lower
            or "ws" in lower
        ):
            important_files.append(file)

    for file in analysis["backend_files"]:
        lower = file.lower()

        if (
            "main.py" in lower
            or "diagnostics" in lower
            or "recovery" in lower
            or "safe_" in lower
            or "memory" in lower
        ):
            important_files.append(file)

    memory["important_files"] = sorted(
        list(set(important_files))
    )

    systems = []

    backend_names = " ".join(
        analysis["backend_files"]
    ).lower()

    frontend_names = " ".join(
        analysis["frontend_files"]
    ).lower()

    if "tts" in backend_names:
        systems.append(
            "Text-to-speech system"
        )

    if "diagnostic" in backend_names:
        systems.append(
            "Diagnostics system"
        )

    if "recovery" in backend_names:
        systems.append(
            "Recovery system"
        )

    if "backup" in backend_names:
        systems.append(
            "Backup system"
        )

    if "rollback" in backend_names:
        systems.append(
            "Rollback protection system"
        )

    if "safe_" in backend_names:
        systems.append(
            "Safe AI editing system"
        )

    if "orb" in frontend_names:
        systems.append(
            "Cinematic orb renderer"
        )

    if "voice" in frontend_names:
        systems.append(
            "Voice interaction system"
        )

    if "ws" in frontend_names:
        systems.append(
            "Realtime websocket system"
        )

    memory["systems"] = sorted(
        list(set(systems))
    )

    architecture_notes = [
        (
            "Frontend uses React + Tauri + "
            "TypeScript for desktop UI rendering."
        ),
        (
            "Backend uses FastAPI for "
            "AI orchestration and tooling."
        ),
        (
            "Orb visualization is powered "
            "by Three.js particle rendering."
        ),
        (
            "Project includes safe AI "
            "editing with rollback protection."
        ),
        (
            "Project supports diagnostics "
            "and recovery workflows."
        ),
        (
            "Project integrates local Ollama "
            "LLM inference."
        ),
    ]

    memory["architecture_notes"] = architecture_notes

    save_memory(memory)

    return {
        "success": True,
        "memory_file": MEMORY_FILE,
        "summary": memory["project_summary"],
        "systems": memory["systems"],
        "important_files": memory["important_files"],
    }


def get_project_memory():
    return load_memory()


def summarize_project_memory():
    memory = load_memory()

    systems_text = "\n".join(
        f"- {system}"
        for system in memory["systems"]
    )

    important_text = "\n".join(
        f"- {file}"
        for file in memory["important_files"]
    )

    notes_text = "\n".join(
        f"- {note}"
        for note in memory["architecture_notes"]
    )

    summary = memory["project_summary"]

    return (
        "JARVIS PROJECT MEMORY\n\n"
        f"Updated: {memory['updated_at']}\n\n"
        "PROJECT SUMMARY\n"
        f"- Total files: {summary.get('total_files', 0)}\n"
        f"- Frontend files: {summary.get('frontend_count', 0)}\n"
        f"- Backend files: {summary.get('backend_count', 0)}\n"
        f"- Other files: {summary.get('other_count', 0)}\n\n"
        "SYSTEMS\n"
        f"{systems_text or '- None'}\n\n"
        "IMPORTANT FILES\n"
        f"{important_text or '- None'}\n\n"
        "ARCHITECTURE NOTES\n"
        f"{notes_text or '- None'}"
    )