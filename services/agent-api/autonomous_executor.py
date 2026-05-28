from autonomous_session import (
    load_autonomous_session,
    update_autonomous_session,
)


def get_next_step(session: dict):
    plan = session.get("plan", {})
    steps = plan.get("steps", [])
    current_step = session.get("current_step", 0)

    if current_step >= len(steps):
        return None

    return steps[current_step]


def preview_next_autonomous_step():
    session = load_autonomous_session()

    if not session:
        return {
            "success": False,
            "error": "No autonomous session found. Create one with: plan autonomous YOUR GOAL",
        }

    step = get_next_step(session)

    if not step:
        session["status"] = "completed"
        update_autonomous_session(session)

        return {
            "success": True,
            "completed": True,
            "message": "Autonomous session is already completed.",
            "session": session,
        }

    return {
        "success": True,
        "completed": False,
        "step": step,
        "session": session,
    }


def mark_next_step_complete():
    session = load_autonomous_session()

    if not session:
        return {
            "success": False,
            "error": "No autonomous session found.",
        }

    step = get_next_step(session)

    if not step:
        session["status"] = "completed"
        update_autonomous_session(session)

        return {
            "success": True,
            "message": "No remaining steps. Session marked completed.",
            "session": session,
        }

    completed_steps = session.get("completed_steps", [])
    completed_steps.append(step)

    session["completed_steps"] = completed_steps
    session["current_step"] = session.get("current_step", 0) + 1

    plan = session.get("plan", {})
    steps = plan.get("steps", [])

    if session["current_step"] >= len(steps):
        session["status"] = "completed"
    else:
        session["status"] = "in_progress"

    update_autonomous_session(session)

    return {
        "success": True,
        "message": "Autonomous step marked complete.",
        "completed_step": step,
        "session": session,
    }


def format_next_autonomous_step(result: dict):
    if not result.get("success"):
        return f"Autonomous Executor Error:\n{result.get('error')}"

    if result.get("completed"):
        return result.get("message", "Autonomous session completed.")

    step = result.get("step", {})

    target_files = step.get("target_files", [])
    target_text = "\n".join(
        [f"- {file}" for file in target_files]
    )

    return (
        "NEXT AUTONOMOUS STEP\n\n"
        f"Step: {step.get('step', 'Unknown')}\n"
        f"Title: {step.get('title', 'Untitled step')}\n"
        f"Type: {step.get('action_type', 'unknown')}\n"
        f"Requires Backup: {step.get('requires_backup', True)}\n\n"
        "Target Files:\n"
        f"{target_text or '- None listed'}\n\n"
        "Description:\n"
        f"{step.get('description', 'No description provided.')}\n\n"
        "Status:\n"
        "Preview only. No files were changed."
    )


def format_step_completion(result: dict):
    if not result.get("success"):
        return f"Autonomous Executor Error:\n{result.get('error')}"

    step = result.get("completed_step", {})

    return (
        "AUTONOMOUS STEP COMPLETED\n\n"
        f"Completed: {step.get('title', 'Unknown step')}\n"
        f"Status: {result.get('session', {}).get('status', 'unknown')}\n"
        f"Current Step Index: {result.get('session', {}).get('current_step', 0)}"
    )