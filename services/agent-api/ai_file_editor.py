import os

from openai import OpenAI

from ai_response_cleaner import clean_ai_file_content


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def improve_file_with_ai(
    path: str,
    instruction: str
):
    if not os.path.exists(path):
        return {
            "success": False,
            "error": "File not found."
        }

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        current_content = file.read()

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer. "
                    "Rewrite the provided file based on the user's instruction. "
                    "Return ONLY the complete updated raw file content. "
                    "Do not include markdown fences. "
                    "Do not explain anything."
                )
            },
            {
                "role": "user",
                "content": (
                    f"File path:\n{path}\n\n"
                    f"Current file content:\n{current_content}\n\n"
                    f"Instruction:\n{instruction}\n\n"
                    "Return the complete updated file content only."
                )
            }
        ]
    )

    raw_content = (
        response
        .choices[0]
        .message
        .content
    )

    updated_content = clean_ai_file_content(
        raw_content
    )

    if not updated_content.strip():
        return {
            "success": False,
            "error": (
                "AI returned empty file content."
            )
        }

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(updated_content)

    return {
        "success": True,
        "path": path
    }