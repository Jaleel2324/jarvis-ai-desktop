import os

from openai import OpenAI

from ai_response_cleaner import clean_ai_file_content


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def ensure_parent(path: str):
    parent = os.path.dirname(path)

    if parent:
        os.makedirs(
            parent,
            exist_ok=True
        )


def generate_file_content(
    path: str,
    instruction: str
):
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer. "
                    "Generate ONLY the complete raw file content. "
                    "Do not include markdown fences. "
                    "Do not explain anything."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"File path: {path}\n\n"
                    f"User instruction:\n{instruction}\n\n"
                    "Return the full complete file content only."
                ),
            },
        ],
    )

    raw_content = (
        response
        .choices[0]
        .message
        .content
    )

    cleaned = clean_ai_file_content(
        raw_content
    )

    if not cleaned.strip():
        raise ValueError(
            "AI returned empty file content."
        )

    return cleaned


def generate_file(
    path: str,
    instruction: str
):
    ensure_parent(path)

    content = generate_file_content(
        path,
        instruction
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(content)

    return {
        "success": True,
        "path": path,
        "content": content,
    }