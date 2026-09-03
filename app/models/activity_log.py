from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base


class ActivityLogModel(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String(50), nullable=False)

    description = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    user = relationship("UserModel")