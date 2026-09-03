from sqlalchemy.orm import Session

from models.user import UserModel
from core.exceptions import NotFoundException


def get_profile_service(current_user: UserModel):
    return current_user


def get_users_service(db: Session, name: str | None = None, email: str | None = None, is_active: bool | None = None):
    query = db.query(UserModel)

    if name:
        name = name.strip()
        query = query.filter(UserModel.full_name.ilike(f"%{name}%"))

    if email:
        email = email.strip()
        query = query.filter(UserModel.email.ilike(f"%{email}%"))

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    return query.all()

