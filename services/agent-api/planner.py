from openai import OpenAI
from conversation import PlanningSession

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def generate_project_plan(session: PlanningSession) -> str:
    context = session.get_context()

    prompt = f"""
You are JARVIS, an elite AI software architect.

Based on this planning session, generate:

1. Recommended project architecture
2. Suggested folders/files
3. Recommended technologies
4. Main features
5. Development phases
6. Backend structure
7. Frontend structure
8. Database recommendations
9. Deployment suggestions

PLANNING CONTEXT:
{context}
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an advanced AI architect helping build "
                    "premium futuristic software systems."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content