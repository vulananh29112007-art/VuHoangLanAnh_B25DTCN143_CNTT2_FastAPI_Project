from datetime import datetime

from sqlalchemy.orm import Session

from models.activity import ClubActivityModel
from models.club import ClubModel
from models.member import ClubMemberModel
from models.user import UserModel

from core.exceptions import (
    NotFoundException,
    ForbiddenException
)


def create_activity_service(
    db: Session,
    club_id: int,
    data,
    current_user: UserModel
):
    # 1. Kiểm tra CLB có tồn tại không
    club = (
        db.query(ClubModel)
        .filter(ClubModel.id == club_id)
        .first()
    )

    if not club:
        raise NotFoundException(
            "Câu lạc bộ không tồn tại"
        )

    # 2. Kiểm tra người tạo có phải member của CLB không
    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise ForbiddenException(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    # 3. Tạo activity
    activity = ClubActivityModel(
        club_id=club_id,
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        priority=data.priority,
        status="TODO",
        created_at=datetime.now()
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity