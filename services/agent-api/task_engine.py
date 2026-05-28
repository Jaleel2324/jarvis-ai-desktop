import subprocess
import os

from datetime import datetime


TASK_LOG_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "task-logs",
    )
)

os.makedirs(
    TASK_LOG_PATH,
    exist_ok=True
)


class TaskEngine:
    def execute(
        self,
        task_name: str,
        command: str
    ):
        started = datetime.now().isoformat()

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            output = (
                result.stdout
                or result.stderr
                or "Task completed."
            )

            log_path = os.path.join(
                TASK_LOG_PATH,
                f"{task_name}.txt"
            )

            with open(
                log_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(output)

            return {
                "success": result.returncode == 0,
                "task": task_name,
                "output": output[:4000],
                "log": log_path,
                "started": started,
                "return_code": result.returncode,
            }

        except Exception as e:
            return {
                "success": False,
                "task": task_name,
                "error": str(e),
                "started": started
            }


task_engine = TaskEngine()