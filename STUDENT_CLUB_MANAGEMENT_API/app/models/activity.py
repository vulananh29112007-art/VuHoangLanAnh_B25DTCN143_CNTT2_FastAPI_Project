from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from db import Base
from sqlalchemy.orm import relationship

class ClubActivityModel(Base):
    __tablename__ = "club_activities"

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), nullable=False)
    priority = Column(String(20), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)

    club = relationship("ClubModel", back_populates="activities")
    assignee = relationship("UserModel", back_populates="assigned_activities")
