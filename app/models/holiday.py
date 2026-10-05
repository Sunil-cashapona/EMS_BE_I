from enum import Enum
from datetime import date as DateType

from sqlalchemy import Date, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HolidayType(str, Enum):
    NATIONAL = "national"
    PUBLIC = "public"
    OTHER = "other"


class Holiday(Base):
    __tablename__ = "mst_holidays"
    __table_args__ = {"schema": "EMS_DB"}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    holiday_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    date: Mapped[DateType] = mapped_column(
        Date,
        nullable=False
    )

    day: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    holiday_type: Mapped[HolidayType] = mapped_column(
        SQLEnum(
            HolidayType,
            name="holidaytype",
            schema="EMS_DB"
        ),
        nullable=False
    )