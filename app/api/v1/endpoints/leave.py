from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    get_current_user,
    authorization_user,
)

from app.services.leave import (
    leave_balance,
    apply_leave,
    get_my_leave_applications,
    get_all_leave_applications,
    update_leave_status,
)

from app.models.leave_request import LeaveStatus
from app.models.user import User

from app.schemas.leave_request import (
    LeaveApplyRequest,
    LeaveRequestRead,
    LeaveBalanceResponse,
    AdminLeaveRequestRead,
    AdminLeaveApplicationResponse,
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
    return leave_balance(
        db=db,
        user_id=current_user.id
    )


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
    return apply_leave(
        db=db,
        user_id=current_user.id,
        request=request
    )


@router.get(
    "/my-applications",
    response_model=list[LeaveRequestRead]
)
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_leave_applications(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/admin/application",
    response_model=AdminLeaveApplicationResponse
)
def get_applications(
    page: int = 1,
    size: int = 10,
    search: str | None = None,
    status_filter: LeaveStatus | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )

    return get_all_leave_applications(
        db=db,
        page=page,
        size=size,
        search=search,
        status_filter=status_filter,
    )


@router.patch(
    "/{leave_id}/admin/status",
    response_model=LeaveRequestRead
)
def update_leave_status_endpoint(
    leave_id: int,
    status: LeaveStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )

    return update_leave_status(
        db=db,
        leave_id=leave_id,
        new_status=status,
        admin_user_id=current_user.id
    )