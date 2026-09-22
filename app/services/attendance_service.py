from datetime import date

from sqlalchemy.orm import Session

from app.models.attendance import Attendance,AttendanceStatus
from app.models.user import User 

def get_attendance_summary(db: Session, 
                           current_user: User):
    today = date.today()
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



