from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class EmployeeDiretoryResponse(BaseModel):
    employee_id: str
    employee_name: str
    email: str
    dep_id: int  | None = None
    designation_id: int   | None = None
    joining_date: date | None = None
    status: str

model_config = ConfigDict(from_attributes=True)


