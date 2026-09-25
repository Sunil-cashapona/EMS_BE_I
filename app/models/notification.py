from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ---------------------------------------------------------------------------
# Notification Types Enum: Maps database enum values for categories
# ---------------------------------------------------------------------------
class NotificationType(str, PyEnum):
    LEAVE = "leave"
    SALARY = "salary"
    ATTENDANCE = "attendance"
    GENERAL = "general"


# ---------------------------------------------------------------------------
# Notification Model: Maps to 'txn_notifications' table in 'EMS_DB' schema
# ---------------------------------------------------------------------------
class Notification(Base):
    """
    SQLAlchemy ORM model representing in-app notifications.

    Columns:
    - id: Primary key auto-incrementing integer.
    - user_id: Foreign key referencing the recipient user (EMS_DB.txn_user.id).
    - title: Brief headline (e.g. 'Leave Request Approved'). Max 150 chars.
    - message: Full body text of the notification.
    - type: Category enum ('leave', 'salary', 'attendance', 'general').
    - is_read: Boolean flag indicating if recipient has viewed/dismissed this item.
    - created_at: Timestamp when the notification was generated.
    - user: Relationship back to User model.
    """
    __tablename__ = "txn_notifications"
    __table_args__ = {"schema": "EMS_DB"}  

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("EMS_DB.txn_user.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType),
        nullable=False
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    user = relationship(
        "User"
    )
