def mount_component(component_name: str):
    return {
        "success": False,
        "error": (
            "Component mounting is currently disabled because the desktop "
            "frontend is using the reference-style main.ts architecture, "
            "not the older React App.tsx mounting system."
        ),
        "component": component_name
    }