from jarvis_logger import log_action


def log_command(command: str):
    return log_action(
        "COMMAND",
        command
    )


def log_error(error: str):
    return log_action(
        "ERROR",
        error
    )


def log_file_edit(path: str):
    return log_action(
        "FILE_EDIT",
        path
    )


def log_component(component: str):
    return log_action(
        "COMPONENT_ACTION",
        component
    )


def log_task(task: str):
    return log_action(
        "TASK",
        task
    )