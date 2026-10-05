from math import ceil

from sqlalchemy import or_
from  sqlalchemy.orm import Session
from app.models.user import User



def get_employee_directory(
        db: Session,
        page: int=1,
        size: int=10,
        search: str | None= None,
        dep_id: int | None= None,
    ):

    query = db.query(User)

    if search  and search.strip():
        search_value = f"%{search.strip()}%"
        query = query.filter(
            or_(
                User.first_name.ilike(search_value),
                User.last_name.ilike(search_value),
                User.email.ilike(search_value),
                User.employee_id.ilike(search_value),
            )
        )

    if dep_id is not     None:
        query = query.filter(User.dep_id == dep_id)

    

    total = query.count()

    offset = (page - 1) * size
    users = (
        query
        .order_by(User.id.asc())
        .offset(offset)
        .limit(size)
        .all()
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


    total_pages = (
        ceil(total / size)
        if total > 0
        else 0
    )

    return {
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages,
        "employees": employees,
    }
