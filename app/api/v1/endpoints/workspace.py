from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.timezone import get_current_localized_time
from app.models.user import User
from app.models.holiday import Holiday
from app.models.leave_request import LeaveRequest

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

    # Dynamic lookups via joined relationships
    department_name = (
        current_user.department_ref.reference_value
        if current_user.department_ref
        else None
    )
    designation_name = (
        current_user.designation_ref.reference_value
        if current_user.designation_ref
        else None
    )

    shift_status = get_today_attendance(db=db, current_user=current_user)
    attendance_summary = get_attendance_summary(db=db, current_user=current_user)
    leave_balances = get_leave_balance(db=db, current_user=current_user)
    total_remaining_days = sum(item["remaining_days"] for item in leave_balances)

    salaries = get_salary_history(db=db, user_id=current_user.id)
    latest_salary = salaries[0] if salaries else None

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
            "category": "Corporate Holiday"
        }
        for h in upcoming_holidays_db
    ]

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
        "next_holiday": formatted_holidays[0] if formatted_holidays else None,
        "upcoming_holidays": formatted_holidays,
        "recent_leave_requests": recent_leaves,
    }