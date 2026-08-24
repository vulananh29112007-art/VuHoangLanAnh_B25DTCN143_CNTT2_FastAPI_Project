from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class ActivityBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: str = "MEDIUM"

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Tiêu đề hoạt động không được để trống")

        return value


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None
    priority: str | None = None
    status: str | None = None
    assignee_id: int | None = None


class ActivityResponse(ActivityBase):
    id: int
    club_id: int
    assignee_id: int | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)