import json
from datetime import datetime

from openai import OpenAI

from project_memory import summarize_project_memory
from autonomous_session import save_autonomous_session


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def create_autonomous_plan(goal: str):
    if not goal or not goal.strip():
        return {
            "success": False,
            "error": "Goal cannot be empty.",
        }

    project_context = summarize_project_memory()

    prompt = f"""
You are JARVIS, an autonomous software engineering planner.

Your job is to create a safe engineering plan.
Do NOT write code yet.
Do NOT modify files.
Only create a structured plan.

PROJECT MEMORY:
{project_context}

USER GOAL:
{goal}

Return ONLY valid JSON in this format:

{{
  "goal": "...",
  "summary": "...",
  "risk_level": "low | medium | high",
  "estimated_files": ["file1", "file2"],
  "steps": [
    {{
      "step": 1,
      "title": "...",
      "description": "...",
      "action_type": "analyze | create | edit | validate | test",
      "target_files": [],
      "requires_backup": true
    }}
  ],
  "validation": [
    "..."
  ],
  "rollback_plan": [
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
                    "You are JARVIS, a careful autonomous engineering planner. "
                    "You must return valid JSON only."
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
        plan = json.loads(raw)
    except Exception:
        plan = {
            "goal": goal,
            "summary": raw,
            "risk_level": "medium",
            "estimated_files": [],
            "steps": [],
            "validation": [
                "Review plan manually because JSON parsing failed."
            ],
            "rollback_plan": [
                "No automatic rollback plan generated."
            ],
        }

    session = save_autonomous_session(goal, plan)

    return {
        "success": True,
        "created_at": datetime.now().isoformat(),
        "plan": plan,
        "session": session,
    }


def format_autonomous_plan(result: dict):
    if not result.get("success"):
        return f"Autonomous planning failed:\n{result.get('error')}"

    plan = result.get("plan", {})

    steps = plan.get("steps", [])
    validation = plan.get("validation", [])
    rollback = plan.get("rollback_plan", [])

    step_text = "\n".join(
        [
            (
                f"{item.get('step', index + 1)}. "
                f"{item.get('title', 'Untitled step')}\n"
                f"   Type: {item.get('action_type', 'unknown')}\n"
                f"   Files: {', '.join(item.get('target_files', [])) or 'None listed'}\n"
                f"   Backup: {item.get('requires_backup', True)}\n"
                f"   {item.get('description', '')}"
            )
            for index, item in enumerate(steps)
        ]
    )

    validation_text = "\n".join(
        [f"- {item}" for item in validation]
    )

    rollback_text = "\n".join(
        [f"- {item}" for item in rollback]
    )

    estimated_files = "\n".join(
        [f"- {item}" for item in plan.get("estimated_files", [])]
    )

    return (
        "JARVIS AUTONOMOUS ENGINEERING PLAN\n\n"
        f"Goal: {plan.get('goal', 'Unknown')}\n\n"
        f"Summary:\n{plan.get('summary', 'No summary provided.')}\n\n"
        f"Risk Level: {plan.get('risk_level', 'unknown')}\n\n"
        "Estimated Files:\n"
        f"{estimated_files or '- None listed'}\n\n"
        "Steps:\n"
        f"{step_text or '- No steps generated'}\n\n"
        "Validation:\n"
        f"{validation_text or '- No validation listed'}\n\n"
        "Rollback Plan:\n"
        f"{rollback_text or '- No rollback plan listed'}"
    )