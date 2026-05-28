import time

from app_recovery import recover_jarvis_services, format_recovery_report
from process_manager import get_service_status, format_service_status


def launch_production():
    result = recover_jarvis_services()

    print(format_recovery_report(result))

    time.sleep(2)

    status = get_service_status()

    print("")
    print(format_service_status(status))

    return {
        "success": True,
        "recovery": result,
        "status": status,
    }


if __name__ == "__main__":
    launch_production()
