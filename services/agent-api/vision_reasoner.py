from openai import OpenAI
from vision_system import analyze_screen_vision

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def reason_about_screen():
    vision = analyze_screen_vision()

    if not vision.get("success"):
        return {
            "success": False,
            "error": vision.get("error"),
        }

    prompt = f"""
You are JARVIS with Phase 9 real vision.

Analyze this desktop vision data and explain what the user is likely looking at.

VISION DATA:
{vision}

Return:
1. What appears to be on screen
2. What app/window is likely active
3. What the user may be trying to do
4. Important UI regions
5. Possible next actions
6. Any risks or problems visible
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a cinematic AI desktop assistant "
                    "with screen vision and workflow reasoning."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return {
        "success": True,
        "vision": vision,
        "reasoning": response.choices[0].message.content,
    }


def format_vision_reasoning(result):
    if not result.get("success"):
        return f"VISION REASONING ERROR\n\n{result.get('error')}"

    return (
        "PHASE 9 AI VISION REASONING\n\n"
        f"{result.get('reasoning')}"
    )