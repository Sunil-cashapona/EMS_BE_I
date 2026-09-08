from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class NotificationType(str, Enum):
    LEAVE = "leave"
    SALARY = "salary"
    ATTENDANCE = "attendance"
    GENERAL = "general"


class NotificationCreate(BaseModel):
    user_id: int
    title: str = Field(..., max_length=150)
    message: str
    type: NotificationType
    is_read: bool = False
    created_at: datetime | None = None


class NotificationEdit(BaseModel):
    user_id: int | None = None
    title: str | None = Field(default=None, max_length=150)
    message: str | None = None
    type: NotificationType | None = None
    is_read: bool | None = None
    created_at: datetime | None = None


class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)