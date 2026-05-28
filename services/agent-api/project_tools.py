import os
import subprocess


BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)

GENERATED_PROJECTS_PATH = os.path.join(
    BASE_PATH,
    "generated-projects"
)

CODING_PROJECTS_PATH = os.path.join(
    BASE_PATH,
    "workspaces",
    "coding-projects"
)


def open_generated_project(project_name: str):
    safe_name = (
        project_name
        .strip()
        .replace(" ", "-")
        .lower()
    )

    paths_to_check = [
        os.path.join(
            GENERATED_PROJECTS_PATH,
            safe_name
        ),

        os.path.join(
            CODING_PROJECTS_PATH,
            safe_name
        ),
    ]

    for project_path in paths_to_check:
        if os.path.exists(project_path):
            subprocess.Popen(
                ["code", project_path],
                shell=True
            )

            return project_path

    return None