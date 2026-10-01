from  sqlalchemy.orm import Session
from app.models.user import User

from app.schemas.directory import EmployeeDiretoryResponse


def get_employee_directory(db: Session):

    users = (
        db.query(User).order_by
        (User.id.asc()).all()
    )

    employees=[]

    for user in users:
        full_name = user.first_name
        if user.last_name:
            full_name=(
                f"{user.first_name}" 
                f"{user.last_name}"
            )

        employees.append(
            {
                "employee_id":user.employee_id,
                "employee_name":full_name,
                "email":user.email,
                "dep_id":user.dep_id,
                "designation_id":user.designation_id,
                "joining_date":user.joining_date,
                "status":(
                    "Active"
                    if user.is_active
                    else "Inactive"
                ),

            }
        )

    return employees
