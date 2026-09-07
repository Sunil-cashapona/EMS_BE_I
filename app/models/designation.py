from datetime import date

from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Designation(Base):

    __tablename__ = "mst_designation"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    designation_name: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    date_created: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
