from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies.auth import get_current_user

from models.user import UserModel

from schemas.club_schema import ClubCreate, ClubResponse, ClubUpdate

from services.club import (
    create_club_service, 
    get_clubs_service, 
    get_club_detail_service, 
    update_club_service, 
    delete_club_service,
    add_member_service,
    delete_member_service,
    get_members_service
)
from schemas.club_member_schema import (
    ClubMemberCreate,
    ClubMemberResponse
)

router = APIRouter(prefix="/clubs", tags=["Clubs"])


@router.post("", response_model=ClubResponse)
def create_club(
    club_data: ClubCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_club_service(
        db=db,
        club_data=club_data,
        current_user=current_user
    )

@router.get("", response_model=list[ClubResponse])
def get_clubs(
    search: str | None = None,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_clubs_service(
        db=db,
        current_user=current_user,
        search=search
    )

@router.get("/{club_id}", response_model=ClubResponse)
def get_club_detail(
    club_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_club_detail_service(
        db=db,
        club_id=club_id,
        current_user=current_user
    )


@router.patch("/{club_id}", response_model=ClubResponse)
def update_club(
    club_id: int,
    club_data: ClubUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_club_service(
        db=db,
        club_id=club_id,
        club_data=club_data,
        current_user=current_user
    )

@router.delete("/{club_id}")
def delete_club(
    club_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_club_service(
        db=db,
        club_id=club_id,
        current_user=current_user
    )


#member
@router.post("/{club_id}/members", response_model=ClubMemberResponse)
def add_member(
    club_id: int,
    member_data: ClubMemberCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_member_service(
        db=db,
        club_id=club_id,
        user_id=member_data.user_id,
        current_user=current_user
    )


@router.delete("/{club_id}/members/{user_id}")
def delete_member(
    club_id: int,
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_member_service(
        db=db,
        club_id=club_id,
        user_id=user_id,
        current_user=current_user
    )


@router.get("/{club_id}/members")
def get_members(
    club_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_members_service(
        db=db,
        club_id=club_id,
        current_user=current_user
    )