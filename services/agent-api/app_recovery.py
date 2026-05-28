from pathlib import Path

from process_manager import (
    get_service_status,
    start_ollama,
    start_process,
)


def get_project_root():
    return Path(__file__).resolve().parents[2]


def recover_jarvis_services():
    root = get_project_root()
    agent_api = root / "services" / "agent-api"
    desktop_app = root / "apps" / "desktop"

    before = get_service_status()
    actions = []

    if not before["ollama"]["online"]:
        result = start_ollama()
        actions.append({
            "service": "ollama",
            "result": result,
        })

    if not before["backend"]["online"]:
        result = start_process(
            "python main.py",
            cwd=str(agent_api),
            hidden=True,
        )
        actions.append({
            "service": "backend",
            "result": result,
        })

    if not before["frontend"]["online"] and desktop_app.exists():
        result = start_process(
            "npm run dev",
            cwd=str(desktop_app),
            hidden=True,
        )
        actions.append({
            "service": "frontend",
            "result": result,
        })

    after = get_service_status()

    return {
        "success": True,
        "before": before,
        "actions": actions,
        "after": after,
    }


def format_recovery_report(result):
    if not result.get("success"):
        return (
            "JARVIS PRODUCTION RECOVERY FAILED\n\n"
            f"{result.get('error')}"
        )

    before = result.get("before", {})
    after = result.get("after", {})
    actions = result.get("actions", [])

    lines = [
        "JARVIS PRODUCTION RECOVERY",
        "",
        "Before:",
        f"- Backend: {before.get('backend', {}).get('online')}",
        f"- Frontend: {before.get('frontend', {}).get('online')}",
        f"- Ollama: {before.get('ollama', {}).get('online')}",
        "",
        f"Actions taken: {len(actions)}",
    ]

    for item in actions:
        service = item.get("service")
        action_result = item.get("result", {})
        lines.append(
            f"- {service}: success={action_result.get('success')} "
            f"pid={action_result.get('pid')} "
            f"message={action_result.get('message', '')} "
            f"error={action_result.get('error', '')}"
        )

    lines.extend([
        "",
        "After:",
        f"- Backend: {after.get('backend', {}).get('online')}",
        f"- Frontend: {after.get('frontend', {}).get('online')}",
        f"- Ollama: {after.get('ollama', {}).get('online')}",
    ])

    return "\n".join(lines)