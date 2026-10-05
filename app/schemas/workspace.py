from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.schemas.attendance import TodayAttendanceResponse, AttendanceSummaryResponse
from app.schemas.leave_request import LeaveBalanceResponse, LeaveRequestRead
from app.schemas.salary_record import SalaryHistoryResponse

class HolidayBrief(BaseModel):
    id: int
    holiday_name: str
    date: date
    day_name: str
    category: str = "National Holiday"
    model_config = ConfigDict(from_attributes=True)

class WorkspaceResponse(BaseModel):
    # 1. Staff Identity
    employee_id: str
    first_name: str
    full_name: str
    designation: str
    department: str
    
    # 2. Clock & Shift Status
    shift_status: TodayAttendanceResponse
    
    # 3. Monthly Attendance KPI
    attendance_summary: AttendanceSummaryResponse
    
    # 4. Leave Quotas
    total_leave_remaining: int
    leave_balances: list[LeaveBalanceResponse]
    
    # 5. Compensation Snippet & Card
    recent_compensation: SalaryHistoryResponse | None = None
    
    # 6. Holiday Information
    next_holiday: HolidayBrief | None = None
    upcoming_holidays: list[HolidayBrief]
    
    # 7. Recent Time-Off Requests
    recent_leave_requests: list[LeaveRequestRead]
    
    model_config = ConfigDict(from_attributes=True)