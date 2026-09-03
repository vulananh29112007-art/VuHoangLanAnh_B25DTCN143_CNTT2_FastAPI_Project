
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from core.config import secret_key

from models import UserModel
from schemas import UserCreate
from schemas.auth import RegisterUser
from core.security import hash_password
from core.exceptions import BadRequestException
from core.exceptions import BadRequestException
from core.security import verify_password, create_access_token, create_refresh_token


def register_service(db: Session, user_data: RegisterUser):

    # kiểm tra email trùng
    existing_user = db.query(UserModel).filter(
        UserModel.email == user_data.email
    ).first()

    if existing_user:
        raise BadRequestException("Email đã được đăng ký")

    # hash password
    password_hash = hash_password(user_data.password)

    # tạo user
    new_user = UserModel(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Đăng ký thành công",
        "email": new_user.email
    }


# login
def login_service(email: str, password: str, db: Session):

    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        raise BadRequestException(
            "Invalid email or password"
        )

    if not verify_password(password, user.password_hash):
        raise BadRequestException(
            "Invalid email or password"
        )

    if not user.is_active:
        raise BadRequestException(
            "Account is inactive"
        )

    access_token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })

    refresh_token = create_refresh_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role,
        "type": "refresh"
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_token_service(refresh_token: str, db: Session):

    try:
        payload = jwt.decode(
            refresh_token,
            secret_key,
            algorithms=["HS256"]
        )
    except JWTError:
        raise BadRequestException(
            "Refresh token không hợp lệ hoặc đã hết hạn"
        )

    if payload.get("type") != "refresh":
        raise BadRequestException(
            "Token không phải refresh token"
        )

    user_id = payload.get("user_id")

    if user_id is None:
        raise BadRequestException(
            "Refresh token không có user_id"
        )

    user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if user is None:
        raise BadRequestException(
            "User không tồn tại"
        )

    if not user.is_active:
        raise BadRequestException(
            "Account is inactive"
        )

    new_access_token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }