from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from db import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(20), default="USER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    clubs = relationship("ClubModel", back_populates="owner")
    club_members = relationship("ClubMemberModel", back_populates="user")
    assigned_activities = relationship("ClubActivityModel", back_populates="assignee")