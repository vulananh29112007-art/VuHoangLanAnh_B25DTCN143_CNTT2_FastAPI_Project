from datetime import datetime
from sqlalchemy.orm import Session
from .activity_log import create_activity_log_service
from models.club import ClubModel
from models.member import ClubMemberModel
from models.user import UserModel
from schemas.club_schema import ClubCreate, ClubUpdate
from core.exceptions import BadRequestException, NotFoundException, ForbiddenException


def create_club_service(db: Session, club_data: ClubCreate, current_user: UserModel):
    club = ClubModel(
        name=club_data.name.strip(),
        description=club_data.description,
        owner_id=current_user.id,
        created_at=datetime.now()
    )

    db.add(club)
    db.flush()

    member = ClubMemberModel(
        club_id=club.id,
        user_id=current_user.id,
        role="OWNER",
        joined_at=datetime.now()
    )

    db.add(member)

    create_activity_log_service(
        db=db,
        current_user=current_user,
        action="CREATE_CLUB",
        description=f"Tạo câu lạc bộ {club.name}"
    )
    
    db.commit()
    db.refresh(club)

    return club

def get_clubs_service(
    db: Session,
    current_user: UserModel,
    search: str | None = None
):
    if current_user.role == "ADMIN":
        query = db.query(ClubModel)
    else:
        query = (
            db.query(ClubModel)
            .join(
                ClubMemberModel,
                ClubModel.id == ClubMemberModel.club_id
            )
            .filter(
                ClubMemberModel.user_id == current_user.id
            )
        )

    if search:
        search = search.strip()
        query = query.filter(
            ClubModel.name.ilike(f"%{search}%")
        )

    return query.all()

def get_club_detail_service(
    db: Session,
    club_id: int,
    current_user: UserModel
):
    if current_user.role == "ADMIN":
        club = (
            db.query(ClubModel)
            .filter(ClubModel.id == club_id)
            .first()
        )
    else:
        club = (
            db.query(ClubModel)
            .join(
                ClubMemberModel,
                ClubModel.id == ClubMemberModel.club_id
            )
            .filter(
                ClubModel.id == club_id,
                ClubMemberModel.user_id == current_user.id
            )
            .first()
        )

    if not club:
        raise NotFoundException(
            "Câu lạc bộ không tồn tại hoặc bạn không phải thành viên"
        )

    return club


def update_club_service(
    db: Session,
    club_id: int,
    club_data: ClubUpdate,
    current_user: UserModel
):
    club = (
        db.query(ClubModel)
        .filter(ClubModel.id == club_id)
        .first()
    )

    if not club:
        raise NotFoundException("Câu lạc bộ không tồn tại")

    # Kiểm tra người thực hiện có phải OWNER không
    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise ForbiddenException(
            "Chỉ OWNER mới được cập nhật câu lạc bộ"
    )

    if club_data.name is not None:
        club.name = club_data.name.strip()

    if club_data.description is not None:
        club.description = club_data.description



    create_activity_log_service(
        db=db,
        current_user=current_user,
        action="UPDATE_CLUB",
        description=f"Cập nhật câu lạc bộ {club.name}"
    )

    db.commit()
    db.refresh(club)

    return club


def delete_club_service(
    db: Session,
    club_id: int,
    current_user: UserModel
):
    club = (
        db.query(ClubModel)
        .filter(ClubModel.id == club_id)
        .first()
    )

    if not club:
        raise NotFoundException("Câu lạc bộ không tồn tại")

    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise ForbiddenException(
            "Chỉ OWNER mới được xóa câu lạc bộ"
    )

    club_name = club.name

    db.delete(club)

    create_activity_log_service(
        db=db,
        current_user=current_user,
        action="DELETE_CLUB",
        description=f"Xóa câu lạc bộ {club_name}"
    )

    db.commit()

    return {
        "message": "Xóa câu lạc bộ thành công"
    }


# member
def add_member_service(db: Session, club_id: int, user_id: int, current_user: UserModel):
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

    # 2. Chỉ OWNER mới được thêm member
    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise ForbiddenException(
            "Chỉ OWNER mới được thêm thành viên"
    )

    # 3. Kiểm tra user cần thêm có tồn tại không
    user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if not user:
        raise NotFoundException(
            "Người dùng không tồn tại"
        )

    # 4. Kiểm tra user đã là member chưa
    existing_member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == user_id
        )
        .first()
    )

    if existing_member:
        raise BadRequestException(
            "Người dùng đã là thành viên của câu lạc bộ"
        )

    # 5. Thêm member
    member = ClubMemberModel(
        club_id=club_id,
        user_id=user_id,
        role="MEMBER",
        joined_at=datetime.now()
    )

    db.add(member)

    create_activity_log_service(
    db=db,
        current_user=current_user,
        action="ADD_MEMBER",
        description=f"Thêm user {user_id} vào câu lạc bộ {club.name}"
    )

    db.commit()
    db.refresh(member)

    return member


def delete_member_service(
    db: Session,
    club_id: int,
    user_id: int,
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

    # 2. Chỉ OWNER mới được xóa member
    if current_user.role != "ADMIN" and club.owner_id != current_user.id:
        raise ForbiddenException(
            "Chỉ OWNER mới được xóa thành viên"
    )

    # 3. Tìm member trong CLB
    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == user_id
        )
        .first()
    )

    if not member:
        raise NotFoundException(
            "Người dùng không phải thành viên của câu lạc bộ"
        )

    # 4. Không cho xóa OWNER
    if member.role == "OWNER":
        raise ForbiddenException(
            "Không thể xóa OWNER của câu lạc bộ"
        )

    # 5. Xóa member
    db.delete(member)

    create_activity_log_service(
        db=db,
        current_user=current_user,
        action="DELETE_MEMBER",
        description=f"Xóa user {user_id} khỏi câu lạc bộ {club.name}"
    )

    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }


def get_members_service(
    db: Session,
    club_id: int,
    current_user: UserModel
):
    # 1. Kiểm tra CLB tồn tại
    club = (
        db.query(ClubModel)
        .filter(ClubModel.id == club_id)
        .first()
    )

    if not club:
        raise NotFoundException(
            "Câu lạc bộ không tồn tại"
        )

    # 2. Kiểm tra người dùng có thuộc CLB không
    member = (
        db.query(ClubMemberModel)
        .filter(
            ClubMemberModel.club_id == club_id,
            ClubMemberModel.user_id == current_user.id
        )
        .first()
    )

    if current_user.role != "ADMIN" and not member:
        raise ForbiddenException(
            "Bạn không phải thành viên của câu lạc bộ"
    )

    # 3. Lấy tất cả thành viên
    members = (
        db.query(ClubMemberModel, UserModel)
        .join(
            UserModel,
            ClubMemberModel.user_id == UserModel.id
        )
        .filter(
            ClubMemberModel.club_id == club_id
        )
        .all()
    )

    # 4. Format response
    return [
        {
            "user_id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": member.role
        }
        for member, user in members
    ]