from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class EmployeeDirectoryResponse(BaseModel):
    employee_id: str
    employee_name: str
    email: str
    dep_id: int  | None = None
    designation_id: int   | None = None
    joining_date: date | None = None
    status: str

model_config = ConfigDict(from_attributes=True)


class EmployeeDirectoryPaginationResponse(BaseModel):
    employees: list[EmployeeDirectoryResponse]
    total: int = Field(..., description="Total number of employees")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of employees per page")
    total_pages: int = Field(..., description="Total number of pages")

