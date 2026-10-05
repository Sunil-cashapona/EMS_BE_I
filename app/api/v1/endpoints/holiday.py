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

from app.models.user import User

from app.schemas.holiday import (
    HolidayCreate,
    HolidayRead,
)

from app.services.holiday import (
    create_holiday,
    get_holidays,
)


router = APIRouter(
    prefix="/holiday",
    tags=["Holiday Management"],
)


@router.post(
    "/",
    response_model=HolidayRead,
    status_code=status.HTTP_201_CREATED
)
def add_holiday(
    request: HolidayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )

    return create_holiday(
        db=db,
        request=request
    )


@router.get(
    "/",
    response_model=list[HolidayRead]
)
def view_holidays(
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_holidays(
        db=db,
        year=year
    )