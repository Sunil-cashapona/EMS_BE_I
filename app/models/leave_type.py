from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LeaveType(Base):

    __tablename__ = "mst_leave_type"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    type_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    max_days_per_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
