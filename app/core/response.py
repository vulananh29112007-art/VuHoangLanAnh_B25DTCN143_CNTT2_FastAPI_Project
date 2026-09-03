from datetime import datetime
from typing import Any


def response_json(
    status_code: int,
    message: str,
    data: Any = None,
    error: Any = None,
    path: str | None = None
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now().isoformat(),
        "path": path
    }