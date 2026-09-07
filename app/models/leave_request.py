from datetime import date, datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LeaveStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveRequest(Base):

    __tablename__ = "txn_leave_request"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=False
    )

    leave_type_id: Mapped[int] = mapped_column(
        ForeignKey("mst_leave_type.id"),
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[LeaveStatus] = mapped_column(
        Enum(LeaveStatus),
        default=LeaveStatus.PENDING,
        nullable=False
    )

    approved: Mapped[int | None] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=True
    )

    applied_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    user = relationship(
        "User",
        foreign_keys=[user_id]
    )

    approver = relationship(
        "User",
        foreign_keys=[approved]
    )

    leave_type = relationship(
        "LeaveType"
    )