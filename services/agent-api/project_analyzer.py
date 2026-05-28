import os


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
    )
)


IGNORE_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    ".venv",
    ".venv311",
    "target",
    ".vite",
    ".vite-temp",
}


IMPORTANT_EXTENSIONS = {
    ".py",
    ".tsx",
    ".ts",
    ".css",
    ".json",
    ".toml",
    ".html",
    ".md",
}


def analyze_project():
    results = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for file in files:
            ext = os.path.splitext(file)[1]

            if ext not in IMPORTANT_EXTENSIONS:
                continue

            full_path = os.path.join(root, file)

            relative_path = os.path.relpath(
                full_path,
                PROJECT_ROOT
            )

            results.append(relative_path)

    frontend_files = [
        file for file in results
        if file.startswith("apps")
    ]

    backend_files = [
        file for file in results
        if file.startswith("services")
    ]

    other_files = [
        file for file in results
        if not file.startswith("apps")
        and not file.startswith("services")
    ]

    return {
        "success": True,
        "total_files": len(results),
        "frontend_files": frontend_files[:80],
        "backend_files": backend_files[:80],
        "other_files": other_files[:40],
    }


def format_project_analysis():
    analysis = analyze_project()

    frontend_text = "\n".join(
        f"- {file}"
        for file in analysis["frontend_files"]
    )

    backend_text = "\n".join(
        f"- {file}"
        for file in analysis["backend_files"]
    )

    other_text = "\n".join(
        f"- {file}"
        for file in analysis["other_files"]
    )

    return (
        "JARVIS PROJECT ANALYSIS\n\n"
        f"Total tracked files: {analysis['total_files']}\n\n"
        "FRONTEND FILES:\n"
        f"{frontend_text or '- None found'}\n\n"
        "BACKEND FILES:\n"
        f"{backend_text or '- None found'}\n\n"
        "OTHER FILES:\n"
        f"{other_text or '- None found'}"
    )