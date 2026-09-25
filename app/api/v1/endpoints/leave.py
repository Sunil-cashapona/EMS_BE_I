from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user,authorization_user

from app.models.leave_request import (
    LeaveRequest,
    LeaveStatus,
)

from app.models.user import User
from app.models.leave_type import LeaveType

from app.schemas.leave_request import (
    LeaveApplyRequest,
    LeaveRequestRead,
    LeaveBalanceResponse,
    AdminLeaveRequestRead
)


router = APIRouter(
    prefix="/leave",
    tags=["Leave Management"],
)




@router.get(
    "/balance",
    response_model=list[LeaveBalanceResponse]
)
def get_leave_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
                LeaveRequest.user_id == current_user.id,
                LeaveRequest.leave_type_id == leave_type.id,
                LeaveRequest.status == LeaveStatus.APPROVED
            )
            .all()
        )

        # Calculate used days
        used_days = 0

        for leave in approved_leaves:
            used_days += (
                leave.end_date - leave.start_date
            ).days + 1

        # Calculate remaining days
        remaining_days = (
            leave_type.max_days_per_year - used_days
        )

        result.append(
            {
                "leave_type_id": leave_type.id,
                "leave_type_name": leave_type.type_name,
                "total_days": leave_type.max_days_per_year,
                "used_days": used_days,
                "remaining_days": max(remaining_days, 0)
            }
        )

    return result




@router.post(
    "/apply",
    response_model=LeaveRequestRead,
    status_code=status.HTTP_201_CREATED
)
def apply_for_leave(
    request: LeaveApplyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    

    if request.start_date > request.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date cannot be after end date."
        )

    

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
            detail="Leave type not found."
        )

    

    requested_days = (
        request.end_date - request.start_date
    ).days + 1

    

    overlapping_leave = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == current_user.id,

            LeaveRequest.status.in_([
                LeaveStatus.PENDING,
                LeaveStatus.APPROVED
            ]),

            LeaveRequest.start_date <= request.end_date,
            LeaveRequest.end_date >= request.start_date
        )
        .first()
    )

    if overlapping_leave:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a leave request for these dates."
        )

    

    approved_leaves = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.leave_type_id == request.leave_type_id,
            LeaveRequest.user_id == current_user.id,
            LeaveRequest.status == LeaveStatus.APPROVED
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

    

    if requested_days > remaining_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Only {remaining_days} days remaining "
                f"for {leave_type.type_name}."
            )
        )

    

    leave = LeaveRequest(
        user_id=current_user.id,
        leave_type_id=leave_type.id,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
        status=LeaveStatus.PENDING,
        approved=None,
        applied_at=datetime.utcnow()
    )

    

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave




@router.get(
    "/my-applications",
    response_model=list[LeaveRequestRead]
)
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == current_user.id
        )
        .order_by(
            LeaveRequest.applied_at.desc()
        )
        .all()
    )


@router.get("/admin/application")
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )

    applications=(
        db.query(LeaveRequest).order_by(LeaveRequest.applied_at.desc()).all()


    )

    result = []

    for application in applications:

        user = (
            db.query(User)
            .filter(
                User.id == application.user_id
            )
            .first()
        )

        leave_type = (
            db.query(LeaveType)
            .filter(
                LeaveType.id == application.leave_type_id
            )
            .first()
        )

        if not user:
            continue

        if not leave_type:
            continue

        number_of_days = (
            application.end_date -
            application.start_date
        ).days + 1

        employee_name = (
            f"{user.first_name} "
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

                applied_at=application.applied_at
            )
        )

    return result




