from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserLIC(Base):

    __tablename__ = "txn_user_lic"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=False
    )

    policy_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    user = relationship(
        "User"
    )
