from datetime import date as DateType

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Holiday(Base):

    __tablename__ = "mst_holidays"

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