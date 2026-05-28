from openai import OpenAI
from project_analyzer import analyze_project


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def create_refactor_plan(instruction: str):
    analysis = analyze_project()

    frontend_files = "\n".join(
        analysis["frontend_files"][:60]
    )

    backend_files = "\n".join(
        analysis["backend_files"][:60]
    )

    prompt = f"""
You are JARVIS, an autonomous software refactor planner.

User refactor request:
{instruction}

Project files:

FRONTEND:
{frontend_files}

BACKEND:
{backend_files}

Create a safe refactor plan.

Return:
1. Goal
2. Files likely affected
3. Step-by-step plan
4. Risk level
5. Recommended command sequence

Do not edit files yet.
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior software architect. "
                    "Plan refactors safely. Do not write code yet."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content