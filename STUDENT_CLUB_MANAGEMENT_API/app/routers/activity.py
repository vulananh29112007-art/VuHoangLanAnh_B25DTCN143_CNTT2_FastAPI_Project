from fastapi import APIRouter, Depends

from db import get_db
from dependencies.auth import get_current_user

from models.user import UserModel

from schemas.activity_schema import (
    ActivityCreate,
    ActivityResponse
)

from services.activity import create_activity_service


router = APIRouter(
    prefix="/clubs",
    tags=["Club Activities"]
)


@router.post(
    "/{club_id}/activities",
    response_model=ActivityResponse
)
def create_activity(
    club_id: int,
    data: ActivityCreate,
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db)
):
    return create_activity_service(
        db=db,
        club_id=club_id,
        data=data,
        current_user=current_user
    )