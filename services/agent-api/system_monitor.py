import psutil
import platform
import socket

from datetime import datetime


def get_system_status():
    memory = psutil.virtual_memory()

    disk = psutil.disk_usage("C:\\")

    return {
        "timestamp": datetime.now().isoformat(),

        "system": platform.system(),

        "node": socket.gethostname(),

        "cpu_percent": psutil.cpu_percent(interval=1),

        "memory_percent": memory.percent,

        "memory_used_gb": round(
            memory.used / (1024 ** 3),
            2
        ),

        "memory_total_gb": round(
            memory.total / (1024 ** 3),
            2
        ),

        "disk_percent": disk.percent,

        "disk_used_gb": round(
            disk.used / (1024 ** 3),
            2
        ),

        "disk_total_gb": round(
            disk.total / (1024 ** 3),
            2
        ),

        "boot_time": datetime.fromtimestamp(
            psutil.boot_time()
        ).isoformat()
    }