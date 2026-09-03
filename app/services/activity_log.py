from sqlalchemy.orm import Session

from models.activity_log import ActivityLogModel
from models.user import UserModel


def create_activity_log_service(
    db: Session,
    current_user: UserModel,
    action: str,
    description: str
):
    log = ActivityLogModel(
        user_id=current_user.id,
        action=action,
        description=description
    )

    db.add(log)
    # không có commit ở đây vì commit sẽ được thực hiện trong transaction của endpoint gọi service này

    return log