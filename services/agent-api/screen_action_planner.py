from openai import OpenAI

from screen_analyzer import analyze_current_screen


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def create_screen_action_plan():
    analysis_result = analyze_current_screen()

    if not analysis_result.get("success"):
        return {
            "success": False,
            "error": analysis_result.get("error"),
        }

    analysis = analysis_result.get("analysis", "")

    prompt = f"""
You are JARVIS.

The following is a live desktop analysis.

Your job:
- identify what the user is likely trying to accomplish
- identify blockers/errors
- recommend next actions
- prioritize actions
- recommend debugging steps if coding issues exist
- recommend productivity improvements if applicable

Keep the response concise and structured.

LIVE ANALYSIS:
{analysis}
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, an intelligent desktop operating assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    plan = response.choices[0].message.content

    return {
        "success": True,
        "analysis": analysis,
        "plan": plan,
    }


def format_screen_action_plan(result: dict):
    if not result.get("success"):
        return (
            "SCREEN ACTION PLANNING FAILED\n\n"
            f"Error: {result.get('error')}"
        )

    return (
        "LIVE DESKTOP ACTION PLAN\n\n"
        f"{result.get('plan')}"
    )