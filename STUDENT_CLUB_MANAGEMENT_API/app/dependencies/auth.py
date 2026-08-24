from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db.database import get_db
from models.user import UserModel
from core.config import secret_key
from core.exceptions import UnauthorizedException, ForbiddenException


bearer = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    # 1. Lấy JWT từ Authorization Header
    token = credentials.credentials

    # 2. Decode và kiểm tra JWT
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"]
        )
    except JWTError:
        raise UnauthorizedException(
            "Token không hợp lệ hoặc đã hết hạn"
        )

    # 3. Lấy user_id từ JWT
    user_id = payload.get("user_id")

    if user_id is None:
        raise UnauthorizedException("Token không có user_id")

    # 4. Tìm user trong database
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if user is None:
        raise UnauthorizedException("User không tồn tại")

    # 5. Kiểm tra tài khoản có đang hoạt động không
    if not user.is_active:
        raise ForbiddenException("Tài khoản đã bị khóa")

    return user