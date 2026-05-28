import json
from datetime import datetime

from openai import OpenAI

from autonomous_session import (
    load_autonomous_session,
    update_autonomous_session,
)

from project_memory import summarize_project_memory


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def create_patch_for_current_step():
    session = load_autonomous_session()

    if not session:
        return {
            "success": False,
            "error": (
                "No autonomous session found. "
                "Create one with: plan autonomous YOUR GOAL"
            ),
        }

    plan = session.get("plan", {})
    steps = plan.get("steps", [])
    current_step = session.get("current_step", 0)

    if current_step >= len(steps):
        return {
            "success": False,
            "error": "No remaining autonomous steps to patch.",
        }

    step = steps[current_step]
    project_context = summarize_project_memory()

    prompt = f"""
You are JARVIS, a safe autonomous software engineering patch planner.

You are NOT allowed to directly modify files.
You are only creating a proposed patch plan.

PROJECT MEMORY:
{project_context}

CURRENT AUTONOMOUS SESSION:
{json.dumps(session, indent=2)}

CURRENT STEP:
{json.dumps(step, indent=2)}

Return ONLY valid JSON in this format:

{{
  "step_title": "...",
  "summary": "...",
  "risk_level": "low | medium | high",
  "files_to_modify": [
    {{
      "path": "relative/or/absolute/file/path",
      "reason": "...",
      "operation": "create | edit | review",
      "backup_required": true
    }}
  ],
  "proposed_changes": [
    {{
      "path": "relative/or/absolute/file/path",
      "change_summary": "...",
      "instructions": "Exact high-level instructions for the safe writer."
    }}
  ],
  "validation_required": [
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
                    "You are JARVIS, a cautious autonomous patch planner. "
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
        patch = json.loads(raw)
    except Exception:
        patch = {
            "step_title": step.get("title", "Unknown step"),
            "summary": raw,
            "risk_level": "medium",
            "files_to_modify": [],
            "proposed_changes": [],
            "validation_required": [
                "Review manually because JSON parsing failed."
            ],
            "rollback_notes": [
                "No automatic rollback notes generated."
            ],
        }

    session["last_patch"] = patch
    session["last_patch_created_at"] = datetime.now().isoformat()
    session["status"] = "patch_planned"

    update_autonomous_session(session)

    return {
        "success": True,
        "patch": patch,
        "session": session,
    }


def format_patch_plan(result: dict):
    if not result.get("success"):
        return f"Autonomous Patch Error:\n{result.get('error')}"

    patch = result.get("patch", {})

    files = patch.get("files_to_modify", [])
    proposed = patch.get("proposed_changes", [])
    validation = patch.get("validation_required", [])
    rollback = patch.get("rollback_notes", [])

    files_text = "\n".join(
        [
            (
                f"- {item.get('path', 'Unknown path')}\n"
                f"  Operation: {item.get('operation', 'unknown')}\n"
                f"  Backup Required: {item.get('backup_required', True)}\n"
                f"  Reason: {item.get('reason', 'No reason provided')}"
            )
            for item in files
        ]
    )

    proposed_text = "\n".join(
        [
            (
                f"- {item.get('path', 'Unknown path')}\n"
                f"  Change: {item.get('change_summary', 'No summary')}\n"
                f"  Instructions: {item.get('instructions', 'No instructions')}"
            )
            for item in proposed
        ]
    )

    validation_text = "\n".join(
        [f"- {item}" for item in validation]
    )

    rollback_text = "\n".join(
        [f"- {item}" for item in rollback]
    )

    return (
        "JARVIS AUTONOMOUS PATCH PLAN\n\n"
        f"Step: {patch.get('step_title', 'Unknown step')}\n\n"
        f"Summary:\n{patch.get('summary', 'No summary provided')}\n\n"
        f"Risk Level: {patch.get('risk_level', 'unknown')}\n\n"
        "Files To Modify:\n"
        f"{files_text or '- None listed'}\n\n"
        "Proposed Changes:\n"
        f"{proposed_text or '- None listed'}\n\n"
        "Validation Required:\n"
        f"{validation_text or '- None listed'}\n\n"
        "Rollback Notes:\n"
        f"{rollback_text or '- None listed'}"
    )