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
from app.schemas.attendance import (
    AttendanceRead,
    PunchInResponse,
    PunchOutResponse,
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])

APP_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_current_localized_time():
    return datetime.now(APP_TIMEZONE)


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


# 2. PUNCH OUT: Matches by attendance_id, calculates duration & sets status based on thresholds
@router.patch("/punch-out/{attendance_id}", response_model=PunchOutResponse)
def punch_out(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = get_current_localized_time()

    record = (
        db.query(Attendance)
        .filter(
            Attendance.id == attendance_id,
            Attendance.user_id == current_user.id,
        )
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punch-in record not found for this user.",
        )

    if record.check_out is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already punched out for this session.",
        )

    out_time = now.time()
    record.check_out = out_time

    if record.check_in:
        check_in_dt = datetime.combine(
            record.date, record.check_in, tzinfo=APP_TIMEZONE
        )
        duration_seconds = (now - check_in_dt).total_seconds()

        # Calculate exact hours rounded to 2 decimal places
        hours = round(Decimal(str(duration_seconds)) / Decimal("3600"), 2)
        record.working_hours = hours

        # Status criteria: 9+ hrs = PRESENT, 4.5 to <9 hrs = HALF_DAY, <4.5 hrs = ABSENT
        if hours >= Decimal("9.00"):
            record.status = AttendanceStatus.PRESENT
        elif hours >= Decimal("4.50"):
            record.status = AttendanceStatus.HALF_DAY
        else:
            record.status = AttendanceStatus.ABSENT

    db.commit()
    db.refresh(record)
    return record


# 3. GET ATTENDANCE HISTORY
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


# 4. GET LOGGED-IN EMPLOYEE'S ATTENDANCE
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