from datetime import date
from pydantic import BaseModel, ConfigDict
from app.schemas.attendance import TodayAttendanceResponse, AttendanceSummaryResponse
from app.schemas.leave_request import LeaveBalanceResponse, LeaveRequestRead
from app.schemas.salary_record import SalaryHistoryResponse

class HolidayBrief(BaseModel):
    id: int
    holiday_name: str
    date: date
    day_name: str
    category: str = "Corporate Holiday"
    model_config = ConfigDict(from_attributes=True)

class WorkspaceResponse(BaseModel):
    employee_id: str
    first_name: str
    full_name: str
    designation: str | None = None
    department: str | None = None
    shift_status: TodayAttendanceResponse
    attendance_summary: AttendanceSummaryResponse
    total_leave_remaining: int
    leave_balances: list[LeaveBalanceResponse]
    recent_compensation: SalaryHistoryResponse | None = None
    next_holiday: HolidayBrief | None = None
    upcoming_holidays: list[HolidayBrief]
    recent_leave_requests: list[LeaveRequestRead]
    model_config = ConfigDict(from_attributes=True)