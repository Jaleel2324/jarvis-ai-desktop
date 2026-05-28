import os

from ai_component_editor import improve_component_with_ai
from file_backup import backup_file
from rollback_manager import rollback_file
from syntax_checker import validate_file_syntax


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


def safe_improve_component(component_name: str, instruction: str):
    tsx_path = os.path.join(
        COMPONENT_ROOT,
        f"{component_name}.tsx"
    )

    css_path = os.path.join(
        COMPONENT_ROOT,
        f"{component_name}.css"
    )

    tsx_backup = backup_file(tsx_path)
    css_backup = backup_file(css_path)

    if not tsx_backup["success"]:
        return {
            "success": False,
            "error": tsx_backup["error"]
        }

    if not css_backup["success"]:
        return {
            "success": False,
            "error": css_backup["error"]
        }

    result = improve_component_with_ai(
        component_name,
        instruction
    )

    if not result["success"]:
        rollback_file(
            os.path.basename(tsx_backup["backup"]),
            tsx_path
        )

        rollback_file(
            os.path.basename(css_backup["backup"]),
            css_path
        )

        return {
            "success": False,
            "error": result["error"],
            "rolled_back": True
        }

    syntax = validate_file_syntax(tsx_path)

    if not syntax["success"]:
        rollback_file(
            os.path.basename(tsx_backup["backup"]),
            tsx_path
        )

        rollback_file(
            os.path.basename(css_backup["backup"]),
            css_path
        )

        return {
            "success": False,
            "error": (
                "Component syntax validation failed. "
                "Files were automatically rolled back.\n\n"
                f"{syntax['output']}"
            ),
            "rolled_back": True
        }

    return {
        "success": True,
        "component": component_name,
        "tsx_path": tsx_path,
        "css_path": css_path,
        "tsx_backup": tsx_backup["backup"],
        "css_backup": css_backup["backup"],
        "syntax": syntax["output"],
        "rolled_back": False
    }