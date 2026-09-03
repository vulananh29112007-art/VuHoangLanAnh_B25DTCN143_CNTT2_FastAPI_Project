
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.auth import RegisterUser, RegisterResponse, RefreshTokenRequest
from db.database import get_db
from schemas.user_schema import UserCreate, UserResponse
from services import (
    register_service,
    login_service,
    refresh_token_service
)
from dependencies import get_current_user, require_admin
from models import UserModel

router = APIRouter( prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse)
def register(
    user: RegisterUser,
    db: Session = Depends(get_db)
):
    return register_service(db, user)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return login_service(email, password, db)


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_token_service(data.refresh_token, db)