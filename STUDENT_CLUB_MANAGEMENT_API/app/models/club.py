from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from db import Base
from sqlalchemy.orm import relationship

class ClubModel(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)

    owner = relationship("UserModel", back_populates="clubs")
    members = relationship("ClubMemberModel", back_populates="club", cascade="all, delete-orphan")
    activities = relationship("ClubActivityModel", back_populates="club")
