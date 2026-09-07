from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Date,
    ForeignKey,
    Numeric
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SalaryStructure(Base):

    __tablename__ = "mst_salary_structure"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=False
    )

    basic_salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    hra: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    other_allowances: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    user = relationship(
        "User"
    )
