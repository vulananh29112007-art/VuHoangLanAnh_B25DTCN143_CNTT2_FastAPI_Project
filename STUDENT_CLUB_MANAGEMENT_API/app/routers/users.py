from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth import get_current_user
from dependencies.permissions import require_admin
from models.user import UserModel
from schemas.user_schema import UserResponse
from services import (
    get_profile_service,
    get_users_service
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    return get_profile_service(current_user)


@router.get("", response_model=list[UserResponse], dependencies=[Depends(require_admin)])
def get_users(
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    return get_users_service(
        db=db,
        name=name,
        email=email,
        is_active=is_active
    )