import os


TASK_LOG_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "task-logs",
    )
)


def list_task_logs():
    if not os.path.exists(TASK_LOG_PATH):
        return []

    logs = []

    for file_name in os.listdir(TASK_LOG_PATH):
        if file_name.endswith(".txt"):
            full_path = os.path.join(
                TASK_LOG_PATH,
                file_name
            )

            logs.append({
                "name": file_name.replace(".txt", ""),
                "path": full_path,
                "modified": os.path.getmtime(full_path)
            })

    logs.sort(
        key=lambda item: item["modified"],
        reverse=True
    )

    return logs


def read_task_log(task_name: str):
    log_path = os.path.join(
        TASK_LOG_PATH,
        f"{task_name}.txt"
    )

    if not os.path.exists(log_path):
        return None

    with open(
        log_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()