from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class ActivityBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None

    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"

    assignee_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Tiêu đề hoạt động không được để trống")

        return value


class ActivityCreate(ActivityBase):
    assignee_id: int | None = None


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: datetime | None = None

    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = None

    status: Literal["TODO", "IN_PROGRESS", "DONE"] | None = None

    assignee_id: int | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError(
                "Tiêu đề hoạt động không được để trống"
            )

        if len(value) > 255:
            raise ValueError(
                "Tiêu đề không được vượt quá 255 ký tự"
            )

        return value


class ActivityResponse(ActivityBase):
    id: int
    club_id: int
    status: Literal["TODO", "IN_PROGRESS", "DONE"]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ActivityListResponse(BaseModel):
    items: list[ActivityResponse]
    total: int
    limit: int
    offset: int