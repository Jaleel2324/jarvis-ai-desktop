from openai import OpenAI

from screen_ocr import read_screen_text


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)


def analyze_current_screen():
    ocr_result = read_screen_text()

    if not ocr_result.get("success"):
        return {
            "success": False,
            "error": ocr_result.get("error"),
        }

    screen_text = ocr_result.get("text", "")

    if not screen_text.strip():
        return {
            "success": True,
            "analysis": (
                "No readable text detected on screen."
            ),
            "ocr": ocr_result,
        }

    prompt = f"""
You are JARVIS.

Analyze the user's current desktop screen OCR text.

Your job:
- summarize what the user is likely doing
- identify apps/websites/tools visible
- identify coding activity if present
- identify errors if present
- identify possible next actions
- keep the response practical and concise

SCREEN OCR:
{screen_text[:12000]}
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, an intelligent desktop AI assistant."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    analysis = response.choices[0].message.content

    return {
        "success": True,
        "analysis": analysis,
        "ocr": ocr_result,
    }


def format_screen_analysis(result: dict):
    if not result.get("success"):
        return (
            "SCREEN ANALYSIS FAILED\n\n"
            f"Error: {result.get('error')}"
        )

    return (
        "LIVE SCREEN ANALYSIS\n\n"
        f"{result.get('analysis')}"
    )