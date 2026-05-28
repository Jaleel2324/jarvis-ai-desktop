from datetime import datetime


def create_visual_workflow_plan(screen_summary):
    return {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "workflow": [
            "capture_screen",
            "analyze_ui",
            "identify_targets",
            "build_action_plan",
        ],
        "screen_summary": screen_summary,
    }


def format_visual_workflow(result):
    if not result.get("success"):
        return (
            "VISION WORKFLOW FAILED\n\n"
            f"{result.get('error')}"
        )

    lines = [
        "VISION WORKFLOW",
        "",
        f"Timestamp: {result.get('timestamp')}",
        "",
        "Workflow Steps:"
    ]

    for step in result.get("workflow", []):
        lines.append(f"- {step}")

    lines.extend([
        "",
        "Screen Summary:",
        str(result.get("screen_summary")),
    ])

    return "\n".join(lines)