import json
from datetime import datetime

from openai import OpenAI

from autonomous_session import (
    load_autonomous_session,
    update_autonomous_session,
)

from autonomous_validator import (
    run_autonomous_validation,
)

from project_memory import summarize_project_memory
from jarvis_logger import read_recent_logs


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def create_autonomous_repair_plan():
    session = load_autonomous_session()
    validation = run_autonomous_validation()
    project_context = summarize_project_memory()
    recent_logs = read_recent_logs()

    prompt = f"""
You are JARVIS, an autonomous engineering repair planner.

Your job is to analyze validation failures, recent logs, and project memory.
Do NOT edit files.
Do NOT run commands.
Only create a safe repair plan.

PROJECT MEMORY:
{project_context}

CURRENT AUTONOMOUS SESSION:
{json.dumps(session, indent=2) if session else "No active session"}

VALIDATION RESULT:
{json.dumps(validation, indent=2)}

RECENT LOGS:
{recent_logs}

Return ONLY valid JSON in this format:

{{
  "summary": "...",
  "likely_causes": [
    "..."
  ],
  "risk_level": "low | medium | high",
  "files_to_review": [
    {{
      "path": "...",
      "reason": "..."
    }}
  ],
  "recommended_repairs": [
    {{
      "title": "...",
      "description": "...",
      "target_files": [],
      "repair_type": "manual_review | safe_edit | dependency_check | config_check | rebuild",
      "requires_backup": true
    }}
  ],
  "validation_steps": [
    "..."
  ],
  "rollback_notes": [
    "..."
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a cautious autonomous repair planner. "
                    "Return valid JSON only. Do not include markdown."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        repair_plan = json.loads(raw)
    except Exception:
        repair_plan = {
            "summary": raw,
            "likely_causes": [
                "Repair model returned non-JSON output."
            ],
            "risk_level": "medium",
            "files_to_review": [],
            "recommended_repairs": [],
            "validation_steps": [
                "Review repair output manually."
            ],
            "rollback_notes": [
                "No rollback plan generated."
            ],
        }

    if session:
        session["last_repair_plan"] = repair_plan
        session["last_repair_plan_created_at"] = datetime.now().isoformat()
        session["status"] = "repair_planned"
        update_autonomous_session(session)

    return {
        "success": True,
        "repair_plan": repair_plan,
        "validation": validation,
        "session": session,
    }


def format_repair_plan(result: dict):
    if not result.get("success"):
        return f"Autonomous Repair Error:\n{result.get('error')}"

    repair = result.get("repair_plan", {})
    validation = result.get("validation", {})

    causes = repair.get("likely_causes", [])
    files = repair.get("files_to_review", [])
    repairs = repair.get("recommended_repairs", [])
    validation_steps = repair.get("validation_steps", [])
    rollback_notes = repair.get("rollback_notes", [])

    causes_text = "\n".join(
        [f"- {item}" for item in causes]
    )

    files_text = "\n".join(
        [
            (
                f"- {item.get('path', 'Unknown path')}\n"
                f"  Reason: {item.get('reason', 'No reason provided')}"
            )
            for item in files
        ]
    )

    repairs_text = "\n".join(
        [
            (
                f"- {item.get('title', 'Untitled repair')}\n"
                f"  Type: {item.get('repair_type', 'unknown')}\n"
                f"  Files: {', '.join(item.get('target_files', [])) or 'None listed'}\n"
                f"  Backup: {item.get('requires_backup', True)}\n"
                f"  Description: {item.get('description', 'No description')}"
            )
            for item in repairs
        ]
    )

    validation_text = "\n".join(
        [f"- {item}" for item in validation_steps]
    )

    rollback_text = "\n".join(
        [f"- {item}" for item in rollback_notes]
    )

    validation_status = "PASSED" if validation.get("success") else "FAILED"

    return (
        "JARVIS AUTONOMOUS REPAIR PLAN\n\n"
        f"Current Validation: {validation_status}\n\n"
        f"Summary:\n{repair.get('summary', 'No summary provided')}\n\n"
        f"Risk Level: {repair.get('risk_level', 'unknown')}\n\n"
        "Likely Causes:\n"
        f"{causes_text or '- None listed'}\n\n"
        "Files To Review:\n"
        f"{files_text or '- None listed'}\n\n"
        "Recommended Repairs:\n"
        f"{repairs_text or '- None listed'}\n\n"
        "Validation Steps:\n"
        f"{validation_text or '- None listed'}\n\n"
        "Rollback Notes:\n"
        f"{rollback_text or '- None listed'}"
    )