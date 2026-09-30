from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attendance import Attendance, AttendanceStatus
from app.models.user import User
from app.core.timezone import get_current_localized_time, APP_TIMEZONE


def get_attendance_summary(
    db: Session,
    current_user: User
):
    # FIX: Use the application timezone instead of the server's local timezone.
    now = get_current_localized_time()

    # FIX: Use date objects because Attendance.date is a DATE column.
    today = now.date()
    start_date = today.replace(day=1)

    records = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == current_user.id,
            Attendance.date >= start_date,
            Attendance.date <= today,
        )
        .order_by(Attendance.date.desc())
        .all()
    )

    days_present = sum(
        1
        for record in records
        if record.status == AttendanceStatus.PRESENT
    )

    days_absent = sum(
        1
        for record in records
        if record.status == AttendanceStatus.ABSENT
    )

    total_hours = sum(
        record.working_hours or 0
        for record in records
    )

    if days_present > 0:
        average_hours = total_hours / days_present
    else:
        average_hours = 0

    return {
        "days_present": days_present,
        "days_absent": days_absent,
        "total_hours_logged": total_hours,
        "average_daily_work_hours": average_hours,
    }


def get_attendance_history(
    db: Session,
    current_user: User
):
    attendance_records = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == current_user.id
        )
        .order_by(Attendance.date.desc())
        .all()
    )

    return attendance_records


def get_today_attendance(
    db: Session,
    current_user: User
):
    # FIX: Get today's date using the application's configured timezone.
    today = get_current_localized_time().date()

    record = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == current_user.id,
            Attendance.date == today,
        )
        .first()
    )

    # ============================================================
    # CASE 1: User has NOT punched in today
    # ============================================================
    if not record:
        return {
            "attendance_id": None,
            "date": today,
            "check_in": None,
            "check_out": None,
            "working_hours": None,

            # FIX: This can be None because there is no attendance
            # record yet. The schema has been changed accordingly.
            "status": None,

            "session_status": "not_punched",
        }

    # ============================================================
    # CASE 2: User punched in but has NOT punched out
    # ============================================================
    if record.check_out is None:
        return {
            "attendance_id": record.id,
            "date": record.date,
            "check_in": record.check_in,
            "check_out": None,
            "working_hours": None,
            "status": record.status,

            # User currently has an active attendance session.
            "session_status": "punched_in",
        }

    # ============================================================
    # CASE 3: User punched in AND punched out
    # ============================================================
    # FIX: This return was missing in your original code.
    #
    # After punch-out, record.check_out is NOT None, so the
    # previous function reached the end without returning anything.
    #
    # Python then returned None automatically, which caused:
    #
    # ResponseValidationError:
    # Input should be a valid dictionary or object
    #
    return {
        "attendance_id": record.id,
        "date": record.date,
        "check_in": record.check_in,
        "check_out": record.check_out,
        "working_hours": record.working_hours,
        "status": record.status,

        # Attendance session has been completed.
        "session_status": "completed",
    }
