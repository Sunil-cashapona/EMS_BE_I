from datetime import datetime
from decimal import Decimal
from typing import List
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.attendance import Attendance, AttendanceStatus
from app.models.user import User
from app.schemas.attendance import AttendanceRead

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# Match your company's operational timezone
APP_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_current_localized_time():
    return datetime.now(APP_TIMEZONE)


# 1. PUNCH IN
@router.post(
    "/punch-in",
    response_model=AttendanceRead,
    status_code=status.HTTP_201_CREATED,
)
def punch_in(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = get_current_localized_time()
    today = now.date()

    record = (
        db.query(Attendance)
        .filter(Attendance.user_id == current_user.id, Attendance.date == today)
        .first()
    )
    if record:
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
            detail="Attendance entry already exists for today.",
        )


# 2. PUNCH OUT
@router.patch("/punch-out", response_model=AttendanceRead)
def punch_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = get_current_localized_time()
    today = now.date()

    record = (
        db.query(Attendance)
        .filter(Attendance.user_id == current_user.id, Attendance.date == today)
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No punch-in entry found for today. Please punch in first.",
        )

    if record.check_out is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already punched out for today.",
        )

    record.check_out = now.time()

    if record.check_in:
        check_in_dt = datetime.combine(today, record.check_in, tzinfo=APP_TIMEZONE)
        duration_seconds = (now - check_in_dt).total_seconds()

        # Precise Decimal division
        hours = round(Decimal(str(duration_seconds)) / Decimal("3600"), 2)
        record.working_hours = hours

        if hours < Decimal("4.0"):
            record.status = AttendanceStatus.HALF_DAY
        else:
            record.status = AttendanceStatus.PRESENT

    db.commit()
    db.refresh(record)
    return record


# 3. GET ATTENDANCE (Role-Scoped History)
@router.get("/", response_model=List[AttendanceRead])
def read_attendance_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Attendance)

    user_role = getattr(current_user.role, "value", current_user.role)
    if user_role != "admin":
        query = query.filter(Attendance.user_id == current_user.id)

    return query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()


# 4. GET LOGGED-IN EMPLOYEE'S HISTORY
@router.get("/my", response_model=List[AttendanceRead])
def get_my_attendance_history(
    skip: int = 0,
    limit: int = 31,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Attendance)
        .filter(Attendance.user_id == current_user.id)
        .order_by(Attendance.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )