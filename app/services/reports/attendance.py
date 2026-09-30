from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.user import User

from datetime import time
def get_attendance_report(db: Session):

    attendance_records = (
        db.query(
            Attendance,
            User.employee_id,
            User.first_name,
            User.last_name,
            User.dep_id,
        )
        .join(
            User,
            Attendance.user_id == User.id,
        )
        .order_by(
            Attendance.date.desc(),
            Attendance.id.desc(),
        )
        .all()
    )

    records = []

    present_count = 0
    absent_count = 0
    total_working_hours = 0.0

    for attendance, employee_id, first_name, last_name, dep_id in attendance_records:

        full_name = first_name

        if last_name:
            full_name = f"{first_name} {last_name}"

        working_hours = (
            float(attendance.working_hours)
            if attendance.working_hours is not None
            else 0.0
        )

        status = str(attendance.status)

        # Handle enum values such as AttendanceStatus.PRESENT
        if "." in status:
            status = status.split(".")[-1]

        status = status.capitalize()

        if status.lower() == "present":
            present_count += 1

        if status.lower() == "absent":
            absent_count += 1

        total_working_hours += working_hours

        records.append(
            {
                "date": attendance.date,
                "employee_id": employee_id,
                "employee_name": full_name,
                "department_id": dep_id,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
                "working_hours": working_hours,
                "status": status,
            }
        )

    total_records = len(records)

    # ---------------------------------------
    # Present Rate
    # ---------------------------------------

    if total_records > 0:
        present_rate = round(
            (present_count / total_records) * 100,
            2,
        )
    else:
        present_rate = 0.0

    # ---------------------------------------
    # Average Working Hours
    # ---------------------------------------

    if total_records > 0:
        avg_work_hours = round(
            total_working_hours / total_records,
            2,
        )
    else:
        avg_work_hours = 0.0

    return {
        "summary": {
            "total_records": total_records,
            "present_rate": present_rate,
            "absenteeism": absent_count,
            "avg_work_hours": avg_work_hours,
        },
        "records": records,
    }