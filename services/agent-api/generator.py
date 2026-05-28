from openai import OpenAI
from conversation import PlanningSession

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def generate_project_files(session: PlanningSession) -> str:
    context = session.get_context()

    prompt = f"""
You are JARVIS, an elite AI software engineer.

Generate:

1. Recommended project folder structure
2. Starter files
3. Example frontend structure
4. Example backend structure
5. Example API routes
6. Example database schema
7. Suggested next coding steps

PLANNING CONTEXT:
{context}
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an elite futuristic AI software architect."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content