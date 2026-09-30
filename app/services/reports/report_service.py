from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User

def get_employee_master_report(db: Session):
    
    users = (
        db.query(User).order_by
        (User.id.asc()).all())

    total_headcount = (
        db.query(User.id).count()
    )

    active_status = (
        db.query(User).filter(User.is_active.is_(True)).count()
    )

    departments = (
        db.query(func.count(func.distinct(User.dep_id)))
        .filter(User.dep_id.isnot(None))
        .scalar()
    ) or 0

    employees = []

    for user in users:

        full_name = user.first_name

        if user.last_name:
            full_name = f"{user.first_name} {user.last_name}"

        employees.append(
            {
                "employee_id": user.employee_id,
                "name": full_name,
                "dep_id": user.dep_id,
                "employment_type_id": user.employment_type_id,
                "joining_date": user.joining_date,
                "status": (
                    "Active"
                    if user.is_active
                    else "Inactive"
                ),
            }
        )

    return {
        "summary": {
            "total_headcount": total_headcount,
            "active_status": active_status,
            "departments": departments,
            
        },
        "employees": employees,
    }