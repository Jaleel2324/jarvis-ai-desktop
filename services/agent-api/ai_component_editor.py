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


def improve_component_with_ai(
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

    if not os.path.exists(tsx_path):
        return {
            "success": False,
            "error": f"TSX file not found: {tsx_path}"
        }

    if not os.path.exists(css_path):
        return {
            "success": False,
            "error": f"CSS file not found: {css_path}"
        }

    with open(
        tsx_path,
        "r",
        encoding="utf-8"
    ) as file:
        current_tsx = file.read()

    with open(
        css_path,
        "r",
        encoding="utf-8"
    ) as file:
        current_css = file.read()

    prompt = f"""
Improve this React component and CSS.

Component name:
{component_name}

Instruction:
{instruction}

Current TSX:
{current_tsx}

Current CSS:
{current_css}

Return the answer in this EXACT format:

---TSX---
FULL UPDATED TSX FILE CONTENT HERE
---CSS---
FULL UPDATED CSS FILE CONTENT HERE
"""

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert React TypeScript UI engineer. "
                    "Rewrite both files based on the instruction. "
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
        return {
            "success": False,
            "error": (
                "AI response did not contain clean TSX/CSS sections."
            )
        }

    tsx_content = clean_ai_file_content(
        tsx_content
    )

    css_content = clean_ai_file_content(
        css_content
    )

    if not tsx_content.strip() or not css_content.strip():
        return {
            "success": False,
            "error": (
                "AI returned empty component content."
            )
        }

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