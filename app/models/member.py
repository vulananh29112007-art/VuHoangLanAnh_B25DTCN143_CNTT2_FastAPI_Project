from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base

class ClubMemberModel(Base):
    __tablename__ = "club_members"

    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), nullable=False)
    joined_at = Column(DateTime, nullable=False)

    club = relationship("ClubModel", back_populates="members")
    user = relationship("UserModel", back_populates="club_members")