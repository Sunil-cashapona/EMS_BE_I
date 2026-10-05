from math import ceil

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.leave_request import LeaveRequest, LeaveStatus
from app.models.leave_type import LeaveType
from app.models.user import User

from app.schemas.leave_request import (
    LeaveApplyRequest,
    LeaveBalanceResponse,
    AdminLeaveRequestRead,
)

from app.services.notification_service import create_system_notification
from app.models.notification import NotificationType


def leave_balance(
    db: Session,
    user_id: int
):
    leave_types = (
        db.query(LeaveType)
        .order_by(LeaveType.id)
        .all()
    )

    result = []

    for leave_type in leave_types:

        approved_leaves = (
            db.query(LeaveRequest)
            .filter(
                LeaveRequest.user_id == user_id,
                LeaveRequest.leave_type_id == leave_type.id,
                LeaveRequest.status == LeaveStatus.APPROVED,
            )
            .all()
        )

        used_days = 0

        for leave in approved_leaves:
            used_days += (
                leave.end_date - leave.start_date
            ).days + 1

        remaining_days = (
            leave_type.max_days_per_year - used_days
        )

        result.append(
            LeaveBalanceResponse(
                leave_type_id=leave_type.id,
                leave_type_name=leave_type.type_name,
                max_days_per_year=leave_type.max_days_per_year,
                used_days=used_days,
                remaining_days=max(remaining_days, 0),
            )
        )

    return result


def apply_leave(
    db: Session,
    user_id: int,
    request: LeaveApplyRequest
):

    leave_type = (
        db.query(LeaveType)
        .filter(
            LeaveType.id == request.leave_type_id
        )
        .first()
    )

    if not leave_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave type not found"
        )

    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date"
        )

    number_of_days = (
        request.end_date - request.start_date
    ).days + 1

    approved_leaves = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.leave_type_id == request.leave_type_id,
            LeaveRequest.status == LeaveStatus.APPROVED,
        )
        .all()
    )

    used_days = 0

    for leave in approved_leaves:
        used_days += (
            leave.end_date - leave.start_date
        ).days + 1

    available_days = (
        leave_type.max_days_per_year - used_days
    )

    if number_of_days > available_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Leave limit exceeded. "
                f"Available days: {max(available_days, 0)}"
            )
        )

    overlapping_leave = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.status.in_([
                LeaveStatus.PENDING,
                LeaveStatus.APPROVED,
            ]),
            LeaveRequest.start_date <= request.end_date,
            LeaveRequest.end_date >= request.start_date,
        )
        .first()
    )

    if overlapping_leave:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a leave application for these dates"
        )

    leave = LeaveRequest(
        user_id=user_id,
        leave_type_id=request.leave_type_id,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        status=LeaveStatus.PENDING,
        approved=None,
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave


def get_my_leave_applications(
    db: Session,
    user_id: int
):
    return (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == user_id
        )
        .order_by(
            LeaveRequest.applied_at.desc()
        )
        .all()
    )


def get_all_leave_applications(
    db: Session,
    page: int = 1,
    size: int = 10,
    search: str | None = None,
    status_filter: LeaveStatus | None = None,
):
    query = (
        db.query(
            LeaveRequest,
            User,
            LeaveType
        )
        .join(
            User,
            LeaveRequest.user_id == User.id
        )
        .join(
            LeaveType,
            LeaveRequest.leave_type_id == LeaveType.id
        )
    )

    # Search by:
    # employee first name
    # employee last name
    # employee code
    # employee email
    # leave reason

    if search:
        search_value = f"%{search.strip()}%"

        query = query.filter(
            or_(
                User.first_name.ilike(search_value),
                User.last_name.ilike(search_value),
                User.employee_id.ilike(search_value),
                User.email.ilike(search_value),
                LeaveRequest.reason.ilike(search_value),
            )
        )

    # Status filter
    if status_filter:
        query = query.filter(
            LeaveRequest.status == status_filter
        )

    # Total matching records
    total = query.count()

    # Pagination validation
    if page < 1:
        page = 1

    if size < 1:
        size = 10

    if size > 100:
        size = 100

    # Calculate offset
    offset = (page - 1) * size

    # Get paginated records
    applications = (
        query
        .order_by(
            LeaveRequest.applied_at.desc()
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    result = []

    for application, user, leave_type in applications:

        number_of_days = (
            application.end_date -
            application.start_date
        ).days + 1

        employee_name = (
            f"{user.first_name or ''} "
            f"{user.last_name or ''}"
        ).strip()

        result.append(
            AdminLeaveRequestRead(
                id=application.id,
                user_id=user.id,
                employee_name=employee_name,
                department=None,
                leave_type_id=leave_type.id,
                leave_type=leave_type.type_name,
                start_date=application.start_date,
                end_date=application.end_date,
                number_of_days=number_of_days,
                reason=application.reason,
                status=application.status,
                approved=application.approved,
                applied_at=application.applied_at,
            )
        )

    # Calculate total pages
    total_pages = ceil(total / size) if total > 0 else 0

    return {
        "items": result,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages,
    }


def update_leave_status(
    db: Session,
    leave_id: int,
    new_status: LeaveStatus,
    admin_user_id: int,
):

    leave = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.id == leave_id
        )
        .first()
    )

    if not leave:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found"
        )

    if leave.status != LeaveStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Leave request has already been processed"
        )

    leave.status = new_status

    if new_status == LeaveStatus.APPROVED:
        leave.approved = admin_user_id
    else:
        leave.approved = None

    db.commit()
    db.refresh(leave)

    status_str = (
        "approved"
        if new_status == LeaveStatus.APPROVED
        else "rejected"
    )

    create_system_notification(
        db=db,
        user_id=leave.user_id,
        title=f"Leave Request {status_str.capitalize()}",
        message=(
            f"Your leave request from "
            f"{leave.start_date} to {leave.end_date} "
            f"has been {status_str}."
        ),
        notification_type=NotificationType.LEAVE,
    )

    return leave