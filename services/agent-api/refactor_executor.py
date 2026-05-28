import os

from openai import OpenAI

from file_backup import backup_file
from rollback_manager import rollback_file
from syntax_checker import validate_file_syntax
from ai_response_cleaner import clean_ai_file_content


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)


SAFE_EDIT_EXTENSIONS = {
    ".tsx",
    ".ts",
    ".css",
    ".py",
}


def read_file(path: str):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()


def write_file(
    path: str,
    content: str
):
    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(content)


def safe_refactor_file(
    relative_path: str,
    instruction: str
):
    full_path = os.path.join(
        PROJECT_ROOT,
        relative_path
    )

    full_path = os.path.abspath(
        full_path
    )

    if not full_path.startswith(
        os.path.abspath(PROJECT_ROOT)
    ):
        return {
            "success": False,
            "error": "Blocked unsafe path."
        }

    if not os.path.exists(full_path):
        return {
            "success": False,
            "error": (
                f"File not found: {full_path}"
            )
        }

    extension = os.path.splitext(
        full_path
    )[1].lower()

    if extension not in SAFE_EDIT_EXTENSIONS:
        return {
            "success": False,
            "error": (
                f"Unsupported file type: {extension}"
            )
        }

    backup = backup_file(full_path)

    if not backup["success"]:
        return {
            "success": False,
            "error": backup["error"]
        }

    current_content = read_file(
        full_path
    )

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer. "
                    "Refactor the provided file according to the instruction. "
                    "Return ONLY the full updated file content. "
                    "No markdown fences. No explanations."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"File path:\n{relative_path}\n\n"
                    f"Instruction:\n{instruction}\n\n"
                    f"Current file content:\n{current_content}\n\n"
                    "Return the full updated file content only."
                ),
            },
        ],
    )

    updated_content = clean_ai_file_content(
        response.choices[0].message.content
    )

    if not updated_content.strip():
        rollback_file(
            os.path.basename(
                backup["backup"]
            ),
            full_path
        )

        return {
            "success": False,
            "error": (
                "AI returned empty file content."
            ),
            "file": relative_path,
            "backup": backup["backup"],
            "rolled_back": True,
        }

    write_file(
        full_path,
        updated_content
    )

    syntax = validate_file_syntax(
        full_path
    )

    if not syntax["success"]:
        rollback_file(
            os.path.basename(
                backup["backup"]
            ),
            full_path
        )

        return {
            "success": False,
            "error": (
                "Syntax validation failed. "
                "File was automatically rolled back.\n\n"
                f"{syntax['output']}"
            ),
            "file": relative_path,
            "backup": backup["backup"],
            "rolled_back": True,
        }

    return {
        "success": True,
        "file": relative_path,
        "path": full_path,
        "backup": backup["backup"],
        "syntax": syntax["output"],
        "rolled_back": False,
    }


def safe_refactor_files(
    relative_paths: list[str],
    instruction: str
):
    results = []

    for relative_path in relative_paths:
        result = safe_refactor_file(
            relative_path,
            instruction
        )

        results.append(result)

    success_count = len([
        result for result in results
        if result.get("success")
    ])

    fail_count = (
        len(results) - success_count
    )

    return {
        "success": fail_count == 0,
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results,
    }


def format_refactor_results(result):
    lines = [
        "SAFE MULTI-FILE REFACTOR RESULTS",
        "",
        f"Successful files: {result['success_count']}",
        f"Failed files: {result['fail_count']}",
        "",
    ]

    for item in result["results"]:

        if item.get("success"):
            lines.append(
                f"[OK] {item['file']}"
            )

            lines.append(
                f"Backup: {item['backup']}"
            )

        else:
            lines.append(
                f"[FAILED] "
                f"{item.get('file', 'unknown')}"
            )

            lines.append(
                f"Error: {item.get('error')}"
            )

            if item.get("backup"):
                lines.append(
                    f"Backup: {item['backup']}"
                )

            if item.get("rolled_back"):
                lines.append(
                    "Rollback: completed automatically"
                )

        lines.append("")

    return "\n".join(lines)