from datetime import datetime

from sqlalchemy.orm import Session

from schemas.activity_schema import ActivityUpdate
from models.activity import ClubActivityModel
from models.member import ClubMemberModel
from models.user import UserModel

from core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BadRequestException
)


def create_activity_service(
    db: Session,
    club_id: int,
    data,
    current_user: UserModel
):
    # Kiểm tra người tạo có phải member của CLB không
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

    # Nếu có assignee thì phải là member của CLB
    if data.assignee_id is not None:

        assignee = (
            db.query(ClubMemberModel)
            .filter(
                ClubMemberModel.club_id == club_id,
                ClubMemberModel.user_id == data.assignee_id
            )
            .first()
        )

        if not assignee:
            raise BadRequestException(
                "Assignee phải là thành viên của câu lạc bộ"
            )

    activity = ClubActivityModel(
        club_id=club_id,
        title=data.title,
        description=data.description,
        created_by=current_user.id,
        assignee_id=data.assignee_id,
        due_date=data.due_date,
        priority=data.priority,
        status="TODO",
        created_at=datetime.now()
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_activities_service(
    db: Session,
    club_id: int,
    current_user: UserModel
):
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

    return (
        db.query(ClubActivityModel)
        .filter(
            ClubActivityModel.club_id == club_id
        )
        .all()
    )


def get_activity_service(
    db: Session,
    activity_id: int,
    current_user: UserModel
):
    activity = (
        db.query(ClubActivityModel)
        .filter(ClubActivityModel.id == activity_id)
        .first()
    )

    if not activity:
        raise NotFoundException(
            "Hoạt động không tồn tại"
        )

    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == activity.club_id,
            ClubMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise ForbiddenException(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    return activity



def update_activity_service(
    db: Session,
    activity_id: int,
    data: ActivityUpdate,
    current_user: UserModel
):
    activity = (
        db.query(ClubActivityModel)
        .filter(
            ClubActivityModel.id == activity_id
        )
        .first()
    )

    if not activity:
        raise NotFoundException(
            "Hoạt động không tồn tại"
        )

    # Tìm membership của user hiện tại
    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == activity.club_id,
            ClubMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise ForbiddenException(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    # Chỉ OWNER hoặc người tạo activity mới được sửa
    if (
        member.role != "OWNER"
        and activity.created_by != current_user.id
    ):
        raise ForbiddenException(
            "Bạn không có quyền sửa hoạt động này"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # Nếu thay đổi assignee
    if "assignee_id" in update_data:

        assignee_id = update_data["assignee_id"]

        if assignee_id is not None:

            assignee = (
                db.query(ClubMemberModel)
                .filter(
                    ClubMemberModel.club_id == activity.club_id,
                    ClubMemberModel.user_id == assignee_id
                )
                .first()
            )

            if not assignee:
                raise BadRequestException(
                    "Assignee phải là thành viên của câu lạc bộ"
                )

    for field, value in update_data.items():
        setattr(activity, field, value)

    db.commit()
    db.refresh(activity)

    return activity


def delete_activity_service(
    db: Session,
    activity_id: int,
    current_user: UserModel
):
    activity = (
        db.query(ClubActivityModel)
        .filter(ClubActivityModel.id == activity_id)
        .first()
    )

    if not activity:
        raise NotFoundException(
            "Hoạt động không tồn tại"
        )

    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == activity.club_id,
            ClubMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise ForbiddenException(
            "Bạn không phải thành viên của câu lạc bộ"
        )

    if (member.role != "OWNER" and activity.created_by != current_user.id):
        raise ForbiddenException(
            "Bạn không có quyền xóa hoạt động này"
        )

    db.delete(activity)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Xóa hoạt động thành công"
    }


def search_filter_activities_service(
    db: Session,
    club_id: int,
    current_user: UserModel,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    search: str | None = None
):
    # Kiểm tra user có thuộc CLB không
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

    # Query activity của CLB
    query = (
        db.query(ClubActivityModel)
        .filter(
            ClubActivityModel.club_id == club_id
        )
    )

    # Filter status
    if status:
        query = query.filter(
            ClubActivityModel.status == status
        )

    # Filter priority
    if priority:
        query = query.filter(
            ClubActivityModel.priority == priority
        )

    # Filter assignee
    if assignee_id:
        query = query.filter(
            ClubActivityModel.assignee_id == assignee_id
        )

    # Search theo title
    if search:
        query = query.filter(
            ClubActivityModel.title.ilike(f"%{search}%")
        )

    return query.all()



def paginate_sort_activities_service(
    query,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    # Tổng số activity trước khi phân trang
    total = query.count()

    # Chọn cột để sort
    if sort_by == "due_date":
        sort_column = ClubActivityModel.due_date
    else:
        sort_column = ClubActivityModel.created_at

    # Chọn chiều sort
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Pagination
    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }