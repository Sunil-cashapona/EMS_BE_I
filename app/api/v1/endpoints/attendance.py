
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo
from sqlalchemy.exc import IntegrityError
import os
from fastapi import APIRouter, Depends,HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.attendance import Attendance, AttendanceStatus
from app.models.user import User
from app.core.timezone import get_current_localized_time
from app.schemas.attendance import (
    AttendanceRead,
    PunchInResponse,
    PunchOutResponse,AttendancePageResponse,AttendanceSummaryResponse,
    TodayAttendanceResponse
)
from app.services.attendance_service import (
    get_attendance_summary,
    get_attendance_history,
    get_today_attendance
)


router = APIRouter(prefix="/attendance", tags=["Attendance"])






# 1. PUNCH IN: Returns strictly { "id": int, "check_in": "time" }
@router.post(
    "/punch-in",
    response_model=PunchInResponse,
    status_code=status.HTTP_201_CREATED,
)
def punch_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = get_current_localized_time()
    today = now.date()

    existing = (
        db.query(Attendance)
        .filter(Attendance.user_id == current_user.id, Attendance.date == today)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already punched in for today.",
        )

    attendance_entry = Attendance(
        user_id=current_user.id,
        date=today,
        check_in=now.time(),
        status=AttendanceStatus.PRESENT,
    )

    try:
        db.add(attendance_entry)
        db.commit()
        db.refresh(attendance_entry)
        return attendance_entry
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance record already exists for today.",
        )


# 2. PUNCH OUT: Automatically finds today's attendance record
@router.patch(
    "/punch-out",
    response_model=PunchOutResponse,
)
def punch_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = get_current_localized_time()
    today = now.date()

    # Find today's punch-in record for the logged-in user
    record = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == current_user.id,
            Attendance.date == today,
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not punched in for today.",
        )

    # Prevent duplicate punch-out
    if record.check_out is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already punched out for today.",
        )

    # Set punch-out time
    record.check_out = now.time()

    # Calculate working hours
    if record.check_in:
        check_in_dt = datetime.combine(
            record.date,
            record.check_in,
            tzinfo=APP_TIMEZONE,
        )

        duration_seconds = (
            now - check_in_dt
        ).total_seconds()

        hours = round(
            Decimal(str(duration_seconds)) / Decimal("3600"),
            2,
        )

        record.working_hours = hours

        # Update attendance status
        if hours >= Decimal("9.00"):
            record.status = AttendanceStatus.PRESENT

        elif hours >= Decimal("4.50"):
            record.status = AttendanceStatus.HALF_DAY

        else:
            record.status = AttendanceStatus.ABSENT

    try:
        db.commit()
        db.refresh(record)
        return record

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update attendance record.",
        )

@router.get(
    "",
    response_model=AttendanceSummaryResponse
)
def get_attendance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_attendance_summary(
        db=db,
        current_user=current_user 
    )        

@router.get("/history",
            response_model=list[AttendanceRead])
def attendance_history(db:Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    return get_attendance_history(db=db,
                                  current_user=current_user) 


@router.get("/today", response_model=TodayAttendanceResponse)
def today_attendance(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_today_attendance(db=db,
                                current_user=current_user,)
