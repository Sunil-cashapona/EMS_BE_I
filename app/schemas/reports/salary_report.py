from decimal import Decimal

from pydantic import BaseModel,ConfigDict

class SalaryPayrollReportItem(BaseModel):
    month_year: str
    employee_id: int
    employee_name: str

    basic_salary: Decimal
    gross_salary: Decimal
    deductions: Decimal
    net_disbursed: Decimal

    model_config = ConfigDict(from_attributes=True)

class SalaryPayrollReportSummary(BaseModel):
    total_disbursed_net: Decimal
    pf_deductions_collected: Decimal
    lic_premiums_remitted: Decimal

class SalaryPayrollReportResponse(BaseModel):
    generated_date: str
    summary: SalaryPayrollReportSummary
    records: list[SalaryPayrollReportItem]        