from datetime import datetime

from sqlalchemy.orm import Session

from app.models.attendance import Attendance,AttendanceStatus
from app.models.user import User 
from app.core.timezone import get_current_localized_time,APP_TIMEZONE 
from app.schemas.attendance import AdminAttendanceRead

def get_attendance_summary(db: Session, 
                           current_user: User):
    today = datetime.today()
    start_date = today.replace(day=1)

    records = (db.query(Attendance).filter(
        Attendance.user_id == current_user.id, 
        Attendance.date >= start_date,
        Attendance.date <=today
    ).order_by(Attendance.date.desc())
    .all())

    days_present = sum(1 for record in records 
                       if record.status == AttendanceStatus.PRESENT)
    days_absent = sum(1 for record in records
                      if record.status == AttendanceStatus.ABSENT)
    total_hours = sum(record.working_hours or 0 for record in records)

    if days_present > 0:
        average_hours = total_hours / days_present
    else:
        average_hours = 0
    return {
        "days_present": days_present,
        "days_absent" : days_absent,
        "total_hours_logged" : total_hours,
        "average_daily_work_hours" : average_hours}  

def get_attendance_history(db: Session, current_user: User):
    attendance_records = (db.query(Attendance)
                          .filter(Attendance.user_id == current_user.id)
                          .order_by(Attendance.date.desc())
                          .all()) 
    return attendance_records

def get_today_attendance(db: Session, current_user: User):
    today = datetime.now(APP_TIMEZONE).date() 
    record = (db.query(Attendance)
              .filter(Attendance.user_id == current_user.id,
                      Attendance.date == today,).first()) 
    if not record: 
        return{"attendance_id":None,
               "date":today,
               "check_in":None,
               "check_out":None,
               "working_hours":None,
               "status":None,
               "session_status":"not_punched"}
    
    if record.check_out is None:
        return {"attendance_id":record.id,
                "date": record.date,
                "check_in": record.check_in,
                "check_out":None,
                "working_hours":None,
                "status":record.status,
                "session_status":"punched_in"} 


def get_admin_attendance(
    db: Session,
) -> list[AdminAttendanceRead]:

    records = (
        db.query(Attendance)
        .join(User, Attendance.user_id == User.id)
        .order_by(Attendance.date.desc())
        .all()
    )

    result = []

    for record in records:

        employee_name = record.user.first_name

        if record.user.last_name:
            employee_name += f" {record.user.last_name}"

        result.append(
            AdminAttendanceRead(
                id=record.id,
                user_id=record.user_id,
                employee_name=employee_name,
                date=record.date,
                check_in=record.check_in,
                check_out=record.check_out,
                working_hours=record.working_hours,
                status=record.status,
            )
        )

    return result