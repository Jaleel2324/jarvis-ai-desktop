import os
from typing import List


def ensure_parent(path: str):
    parent = os.path.dirname(path)

    if parent:
        os.makedirs(parent, exist_ok=True)


def create_file(path: str, content: str):

    ensure_parent(path)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return {
        "success": True,
        "path": path,
        "action": "created"
    }


def read_file(path: str):

    if not os.path.exists(path):
        return {
            "success": False,
            "error": "File not found."
        }

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    return {
        "success": True,
        "path": path,
        "content": content
    }


def edit_file(path: str, new_content: str):

    if not os.path.exists(path):
        return {
            "success": False,
            "error": "File not found."
        }

    with open(path, "w", encoding="utf-8") as file:
        file.write(new_content)

    return {
        "success": True,
        "path": path,
        "action": "edited"
    }


def append_file(path: str, content: str):

    ensure_parent(path)

    with open(path, "a", encoding="utf-8") as file:
        file.write(content)

    return {
        "success": True,
        "path": path,
        "action": "appended"
    }


def delete_file(path: str):

    if not os.path.exists(path):
        return {
            "success": False,
            "error": "File not found."
        }

    os.remove(path)

    return {
        "success": True,
        "path": path,
        "action": "deleted"
    }


def list_project_files(root_path: str):

    collected: List[str] = []

    if not os.path.exists(root_path):

        return {
            "success": False,
            "error": "Project path not found."
        }

    for root, dirs, files in os.walk(root_path):

        dirs[:] = [
            d for d in dirs
            if d not in [
                "node_modules",
                ".git",
                "__pycache__",
                "dist",
                "build"
            ]
        ]

        for file in files:

            full_path = os.path.join(
                root,
                file
            )

            collected.append(full_path)

    return {
        "success": True,
        "files": collected
    }