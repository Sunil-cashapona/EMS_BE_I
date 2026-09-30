from datetime import date

from pydantic import BaseModel, ConfigDict

class EmployeeMasterItem(BaseModel):
    employee_id: str
    name: str
    dep_id: int | None = None
    employment_type_id: int | None = None
    joining_date: date
    status: str

    model_config = ConfigDict(from_attributes=True) 

class EmployeeMasterSummary(BaseModel):
    total_headcount: int
    active_status: int
    departments: int
    

class EmployeeMasterReportResponse(BaseModel):
    summary: EmployeeMasterSummary
    employees: list[EmployeeMasterItem]