from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PayrollSettingType(str, Enum):
    TAX = "tax"
    PF = "pf"
    ESI = "esi"


class PayrollSettingCreate(BaseModel):
    type: PayrollSettingType
    rate_percent: Decimal = Field(..., max_digits=5, decimal_places=2)
    effective_from: date


class PayrollSettingEdit(BaseModel):
    type: PayrollSettingType | None = None
    rate_percent: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    effective_from: date | None = None


class PayrollSettingRead(BaseModel):
    id: int
    type: PayrollSettingType
    rate_percent: Decimal
    effective_from: date

    model_config = ConfigDict(from_attributes=True)