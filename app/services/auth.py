
from sqlalchemy.orm import Session

from models import UserModel
from schemas import UserCreate
from schemas.auth import RegisterUser
from core.security import hash_password
from core.exceptions import BadRequestException
from core.exceptions import BadRequestException
from core.security import verify_password, create_access_token


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

    token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }