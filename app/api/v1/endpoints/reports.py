from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import authorization_user

from app.core.database import get_db
from app.models.user import User
from app.schemas.reports.employee_report import EmployeeMasterReportResponse
from app.services.reports.report_service import get_employee_master_report
from app.services.reports.attendance import get_attendance_report
from app.schemas.reports.attdendance_report import AttendanceReportResponse
from app.schemas.reports.leave_report import LeaveReportResponse
from app. services.reports.leave import get_leave_report
router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/employee-master",
    response_model=EmployeeMasterReportResponse,
)
def employee_master_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return get_employee_master_report(db)

@router.get(
    "/attendance",
    response_model=AttendanceReportResponse,
)
def attendance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)

):
    return get_attendance_report(db)

@router.get(
    "/leave",
    response_model=LeaveReportResponse,   
)
def leave_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):
    return get_leave_report(db)