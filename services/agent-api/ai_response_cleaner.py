def clean_ai_file_content(content: str):
    if not content:
        return ""

    cleaned = content.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    cleaned = cleaned.replace("```tsx", "")
    cleaned = cleaned.replace("```ts", "")
    cleaned = cleaned.replace("```python", "")
    cleaned = cleaned.replace("```css", "")
    cleaned = cleaned.replace("```html", "")
    cleaned = cleaned.replace("```", "")

    return cleaned.strip()


def extract_section(raw: str, start_marker: str, end_marker: str | None = None):
    if start_marker not in raw:
        return None

    section = raw.split(start_marker, 1)[1]

    if end_marker and end_marker in section:
        section = section.split(end_marker, 1)[0]

    return clean_ai_file_content(section)