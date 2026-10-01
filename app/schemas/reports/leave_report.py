from datetime import date

from pydantic import BaseModel, ConfigDict

class LeaveReportItem(BaseModel):
    
    employee_name: str
    leave_type_id: int 
    start_date: date
    end_date: date
    days: int
    decision: str

    model_config = ConfigDict(from_attributes=True) 

class LeaveReportSummary(BaseModel):
    total_applied: int
    approved: int
    reject_review: int
    

class LeaveReportResponse(BaseModel):
    summary: LeaveReportSummary
    records: list[LeaveReportItem]