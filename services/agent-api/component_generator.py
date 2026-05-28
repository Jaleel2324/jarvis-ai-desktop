import os

from openai import OpenAI

from ai_response_cleaner import clean_ai_file_content, extract_section


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


COMPONENT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "apps",
        "desktop",
        "src",
        "components",
    )
)


def ensure_parent(path: str):
    parent = os.path.dirname(path)

    if parent:
        os.makedirs(
            parent,
            exist_ok=True
        )


def generate_component_files(
    component_name: str,
    instruction: str
):
    tsx_path = os.path.join(
        COMPONENT_ROOT,
        f"{component_name}.tsx"
    )

    css_path = os.path.join(
        COMPONENT_ROOT,
        f"{component_name}.css"
    )

    prompt = f"""
Create a React TypeScript component and matching CSS.

Component name:
{component_name}

User instruction:
{instruction}

Return the answer in this EXACT format:

---TSX---
FULL TSX FILE CONTENT HERE
---CSS---
FULL CSS FILE CONTENT HERE
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert React and TypeScript engineer. "
                    "Return only the requested file contents. "
                    "No markdown fences. No explanations."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    raw = response.choices[0].message.content

    tsx_content = extract_section(
        raw,
        "---TSX---",
        "---CSS---"
    )

    css_content = extract_section(
        raw,
        "---CSS---"
    )

    if not tsx_content or not css_content:
        raise ValueError(
            "AI response did not contain clean TSX/CSS sections."
        )

    tsx_content = clean_ai_file_content(
        tsx_content
    )

    css_content = clean_ai_file_content(
        css_content
    )

    if not tsx_content.strip() or not css_content.strip():
        raise ValueError(
            "AI returned empty component content."
        )

    ensure_parent(tsx_path)
    ensure_parent(css_path)

    with open(
        tsx_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(tsx_content)

    with open(
        css_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(css_content)

    return {
        "success": True,
        "component": component_name,
        "tsx_path": tsx_path,
        "css_path": css_path,
    }