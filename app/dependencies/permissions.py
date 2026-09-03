from fastapi import Depends

from core.exceptions import ForbiddenException
from dependencies.auth import get_current_user


def require_admin(current_user = Depends(get_current_user)):

    if current_user.role != "ADMIN":
        raise ForbiddenException(
            "Admin permission required"
        )

    return current_user