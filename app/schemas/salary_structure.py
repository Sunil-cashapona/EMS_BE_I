from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SalaryStructureCreate(BaseModel):
    user_id: int
    basic_salary: Decimal = Field(..., max_digits=10, decimal_places=2)
    hra: Decimal = Field(..., max_digits=10, decimal_places=2)
    other_allowances: Decimal = Field(..., max_digits=10, decimal_places=2)
    effective_from: date


class SalaryStructureEdit(BaseModel):
    user_id: int | None = None
    basic_salary: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    hra: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    other_allowances: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    effective_from: date | None = None


class SalaryStructureRead(BaseModel):
    id: int
    user_id: int
    basic_salary: Decimal
    hra: Decimal
    other_allowances: Decimal
    effective_from: date

    model_config = ConfigDict(from_attributes=True)

class CurrentSalaryStructureResponse(BaseModel):
    basic_salary: Decimal
    hra: Decimal
    other_allowances: Decimal
    gross_monthly_earnings: Decimal
    effective_from: date    