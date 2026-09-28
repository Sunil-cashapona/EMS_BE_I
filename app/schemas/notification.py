from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Notification Types: Maps to the database enum 'notificationtype'
# Supported tabs in UI: 'leave', 'salary', 'attendance', 'general'
# ---------------------------------------------------------------------------
class NotificationType(str, Enum):
    LEAVE = "leave"
    SALARY = "salary"
    ATTENDANCE = "attendance"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# Schema for creating/triggering a notification
# ---------------------------------------------------------------------------
class NotificationCreate(BaseModel):
    user_id: int
    title: str = Field(..., max_length=150)
    message: str
    type: NotificationType
    is_read: bool = False
    created_at: datetime | None = None


# ---------------------------------------------------------------------------
# Schema for updating a notification (e.g. marking read/unread)
# ---------------------------------------------------------------------------
class NotificationEdit(BaseModel):
    user_id: int | None = None
    title: str | None = Field(default=None, max_length=150)
    message: str | None = None
    type: NotificationType | None = None
    is_read: bool | None = None
    created_at: datetime | None = None


# ---------------------------------------------------------------------------
# Schema for reading a single notification item
# ---------------------------------------------------------------------------
class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Paginated list response schema with total count and unread badge count
# ---------------------------------------------------------------------------
class NotificationListResponse(BaseModel):
    items: list[NotificationRead]
    total: int
    unread_count: int

    model_config = ConfigDict(from_attributes=True)