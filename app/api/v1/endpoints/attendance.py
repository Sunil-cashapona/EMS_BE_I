from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.attendance import AttendancePageResponse,AttendanceRead
from app.services.attendance_service import get_attendance_summary,get_attendance_history


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.get(
    "",
    response_model=AttendancePageResponse
)
def get_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_attendance_summary(
        db=db,
        user_id=current_user.id
    )        

@router.get("/history",
            response_model=list[AttendanceRead])
def attendance_history(db:Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return get_attendance_history(db=db,
                                  current_user=current_user)
