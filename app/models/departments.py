from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Department(Base):

    __tablename__ = "mst_department"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    dep_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    date_created: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
