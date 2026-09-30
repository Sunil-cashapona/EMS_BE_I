from sqlalchemy.orm import Session

from app.models.leave_request import LeaveRequest, LeaveStatus
from app.models.user import User


def get_leave_report(db: Session):

    leave_requests = (
        db.query(
            LeaveRequest,
            User.first_name,
            User.last_name,
        )
        .join(
            User,
            LeaveRequest.user_id == User.id,
        )
        .order_by(
            LeaveRequest.start_date.desc(),
            LeaveRequest.id.desc(),
        )
        .all()
    )

    records = []

    approved_count = 0
    pending_count = 0

    for leave, first_name, last_name in leave_requests:

        employee_name = first_name

        if last_name:
            employee_name = f"{first_name} {last_name}"

        days = (
            leave.end_date - leave.start_date
        ).days + 1

        decision = leave.status.value

        if leave.status == LeaveStatus.APPROVED:
            approved_count += 1

        elif leave.status == LeaveStatus.PENDING:
            pending_count += 1

        records.append(
            {
                "employee_name": employee_name,
                "leave_type_id": leave.leave_type_id,
                "start_date": leave.start_date,
                "end_date": leave.end_date,
                "days": days,
                "decision": decision,
            }
        )

    total_applied = len(records)

    return {
        "summary": {
            "total_applied": total_applied,
            "approved": approved_count,
            "pending_review": pending_count,
        },
        "records": records,
    }