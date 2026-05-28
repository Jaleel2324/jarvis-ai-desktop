import os


WORKSPACE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "generated-projects",
    )
)


def build_project_structure(project_name: str):
    project_path = os.path.join(
        WORKSPACE_PATH,
        project_name
    )

    folders = [
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/src/styles",
        "backend/routes",
        "backend/models",
        "backend/controllers",
    ]

    files = {
        "README.md": f"# {project_name}",

        "frontend/src/App.tsx":
        (
            "export default function App() { "
            "return <h1>JARVIS PROJECT</h1>; "
            "}"
        ),

        "frontend/src/main.tsx":
        (
            "console.log('JARVIS FRONTEND ONLINE');"
        ),

        "backend/server.py":
        (
            "print('JARVIS BACKEND ONLINE')"
        ),
    }

    os.makedirs(
        project_path,
        exist_ok=True
    )

    for folder in folders:
        os.makedirs(
            os.path.join(project_path, folder),
            exist_ok=True
        )

    for path, content in files.items():
        full_path = os.path.join(
            project_path,
            path
        )

        os.makedirs(
            os.path.dirname(full_path),
            exist_ok=True
        )

        with open(
            full_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)

    return project_path