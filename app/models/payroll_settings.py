from datetime import date
from enum import Enum as PyEnum

from sqlalchemy import Date, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PayrollSettingType(str, PyEnum):
    TAX = "tax"
    PF = "pf"
    ESI = "esi"


class PayrollSetting(Base):

    __tablename__ = "mst_payroll_setting"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    type: Mapped[PayrollSettingType] = mapped_column(
        Enum(PayrollSettingType),
        nullable=False
    )

    rate_percent: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
