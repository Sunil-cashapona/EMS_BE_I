from datetime import date, time

from pydantic import BaseModel


class AttendanceReportItem(BaseModel):
    date: date
    employee_id: str
    employee_name: str
    department_id: int | None = None
    check_in: time | None = None
    check_out: time | None = None
    working_hours: float
    status: str


class AttendanceReportSummary(BaseModel):
    total_records: int
    present_rate: float
    absenteeism: int
    avg_work_hours: float


class AttendanceReportResponse(BaseModel):
    summary: AttendanceReportSummary
    records: list[AttendanceReportItem]