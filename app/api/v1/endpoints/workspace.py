from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.timezone import get_current_localized_time
from app.models.user import User
from app.models.holiday import Holiday
from app.models.leave_request import LeaveRequest
from app.models.reference_value import ReferenceValue

# Re-use existing tested service calculations
from app.services.attendance_service import get_today_attendance, get_attendance_summary
from app.services.salary_service import get_salary_history
from app.api.v1.endpoints.leave import get_leave_balance
from app.schemas.workspace import WorkspaceResponse

router = APIRouter(prefix="/workspace", tags=["Workspace"])

@router.get("/dashboard", response_model=WorkspaceResponse)
def get_workspace_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = get_current_localized_time().date()

    # 1. Dynamic Department and Designation Resolution
    department_name = "Engineering"
    if current_user.dep_id:
        dep_record = db.query(ReferenceValue).filter(ReferenceValue.id == current_user.dep_id).first()
        if dep_record:
            department_name = dep_record.reference_value

    designation_name = "Senior Full Stack Engineer"
    if current_user.designation_id:
        desig_record = db.query(ReferenceValue).filter(ReferenceValue.id == current_user.designation_id).first()
        if desig_record:
            designation_name = desig_record.reference_value

    # 2. Clock & Shift Status
    shift_status = get_today_attendance(db=db, current_user=current_user)

    # 3. Monthly Attendance Summary (9 Days: 0 Absent, 9 Present)
    attendance_summary = get_attendance_summary(db=db, current_user=current_user)

    # 4. Leave Quotas (CL: 8, SL: 6, PL: 12)
    leave_balances = get_leave_balance(db=db, current_user=current_user)
    total_remaining_days = sum(item["remaining_days"] for item in leave_balances)

    # 5. Compensation (August 2026 Disbursed Pay)
    salaries = get_salary_history(db=db, user_id=current_user.id)
    latest_salary = salaries[0] if salaries else None

    # 6. Corporate Holidays
    upcoming_holidays_db = (
        db.query(Holiday)
        .filter(Holiday.date >= today)
        .order_by(Holiday.date.asc())
        .limit(3)
        .all()
    )
    formatted_holidays = [
        {
            "id": h.id,
            "holiday_name": h.holiday_name,
            "date": h.date,
            "day_name": h.date.strftime("%A"),
            "category": "Gazetted" if "Memorial" in h.holiday_name else "National Holiday"
        }
        for h in upcoming_holidays_db
    ]
    next_holiday = formatted_holidays[0] if formatted_holidays else None

    # 7. Recent Time-Off Applications (Latest 3)
    recent_leaves = (
        db.query(LeaveRequest)
        .filter(LeaveRequest.user_id == current_user.id)
        .order_by(LeaveRequest.applied_at.desc())
        .limit(3)
        .all()
    )

    return {
        "employee_id": current_user.employee_id,
        "first_name": current_user.first_name,
        "full_name": f"{current_user.first_name} {current_user.last_name or ''}".strip(),
        "designation": designation_name,
        "department": department_name,
        "shift_status": shift_status,
        "attendance_summary": attendance_summary,
        "total_leave_remaining": total_remaining_days,
        "leave_balances": leave_balances,
        "recent_compensation": latest_salary,
        "next_holiday": next_holiday,
        "upcoming_holidays": formatted_holidays,
        "recent_leave_requests": recent_leaves,
    }