from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ClubMemberCreate(BaseModel):
    user_id: int
    role: str = "MEMBER"


class ClubMemberResponse(BaseModel):
    club_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)