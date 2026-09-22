from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SalaryStatus(str, Enum):
    GENERATED = "generated"
    PAID = "paid"


class SalaryRecordCreate(BaseModel):
    user_id: int
    month_year: str = Field(..., max_length=7)
    basic_salary: Decimal = Field(..., max_digits=10, decimal_places=2)
    allowances: Decimal = Field(..., max_digits=10, decimal_places=2)
    deductions: Decimal = Field(..., max_digits=10, decimal_places=2)
    tax: Decimal = Field(..., max_digits=10, decimal_places=2)
    pf: Decimal = Field(..., max_digits=10, decimal_places=2)
    esi: Decimal = Field(..., max_digits=10, decimal_places=2)
    lic_deductions: Decimal = Field(..., max_digits=10, decimal_places=2)
    net_salary: Decimal = Field(..., max_digits=10, decimal_places=2)
    payment_date: date | None = None
    payslip_file: str | None = Field(default=None, max_length=255)
    status: SalaryStatus = SalaryStatus.GENERATED


class SalaryRecordEdit(BaseModel):
    user_id: int | None = None
    month_year: str | None = Field(default=None, max_length=7)
    basic_salary: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    allowances: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    deductions: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    tax: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    pf: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    esi: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    lic_deductions: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    net_salary: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    payment_date: date | None = None
    payslip_file: str | None = Field(default=None, max_length=255)
    status: SalaryStatus | None = None


class SalaryRecordRead(BaseModel):
    id: int
    user_id: int
    month_year: str
    basic_salary: Decimal
    allowances: Decimal
    deductions: Decimal
    tax: Decimal
    pf: Decimal
    esi: Decimal
    lic_deductions: Decimal
    net_salary: Decimal
    payment_date: date | None = None
    payslip_file: str | None = None
    status: SalaryStatus

    model_config = ConfigDict(from_attributes=True)