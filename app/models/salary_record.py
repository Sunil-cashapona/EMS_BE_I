from datetime import date
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Numeric,
    String
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SalaryStatus(str, PyEnum):
    GENERATED = "generated"
    PAID = "paid"


class SalaryRecord(Base):

    __tablename__ = "txn_salary_records"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("txn_user.id"),
        nullable=False
    )

    month_year: Mapped[str] = mapped_column(
        String(7),
        nullable=False
    )

    basic_salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    allowances: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    deductions: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    pf: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    esi: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    lic_deductions: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    net_salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    payment_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    payslip_file: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[SalaryStatus] = mapped_column(
        Enum(SalaryStatus),
        default=SalaryStatus.GENERATED,
        nullable=False
    )

    user = relationship(
        "User"
    )
