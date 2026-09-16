from datetime import date as DateType, time as TimeType
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Time
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AttendanceStatus(str, PyEnum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class Attendance(Base):

    __tablename__ = "txn_attendence"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=False
    )

    date: Mapped[DateType] = mapped_column(
        Date,
        nullable=False
    )

    check_in: Mapped[TimeType | None] = mapped_column(
        Time,
        nullable=True
    )

    check_out: Mapped[TimeType | None] = mapped_column(
        Time,
        nullable=True
    )

    working_hours: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )

    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus),
        nullable=False
    )

    user = relationship(
        "User"
    )
