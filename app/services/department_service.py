from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentEdit


def create_department(db: Session, department_data: DepartmentCreate) -> Department:
    normalized_name = department_data.dep_name.strip()

    existing = (
        db.query(Department)
        .filter(func.lower(Department.dep_name) == normalized_name.lower())
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with name '{normalized_name}' already exists",
        )

    dept_dict = department_data.model_dump()
    if not dept_dict.get("date_created"):
        dept_dict["date_created"] = date.today()

    new_department = Department(**dept_dict)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


def get_departments(db: Session, search: str | None = None) -> list[Department]:
    query = db.query(Department)
    if search:
        query = query.filter(Department.dep_name.ilike(f"%{search.strip()}%"))
    return query.order_by(Department.id.asc()).all()


def get_department_by_id(db: Session, department_id: int) -> Department:
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found",
        )
    return department


def update_department(
    db: Session,
    department_id: int,
    department_data: DepartmentEdit,
) -> Department:
    department = get_department_by_id(db, department_id)

    update_dict = department_data.model_dump(exclude_unset=True)

    if "dep_name" in update_dict and update_dict["dep_name"]:
        normalized_name = update_dict["dep_name"].strip()
        existing = (
            db.query(Department)
            .filter(
                func.lower(Department.dep_name) == normalized_name.lower(),
                Department.id != department_id,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department with name '{normalized_name}' already exists",
            )
        update_dict["dep_name"] = normalized_name

    for field, value in update_dict.items():
        setattr(department, field, value)

    db.commit()
    db.refresh(department)
    return department


def delete_department(db: Session, department_id: int) -> dict:
    department = get_department_by_id(db, department_id)

    try:
        db.delete(department)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete department because it is referenced by other records (e.g. employees)",
        )

    return {
        "message": "Department deleted successfully",
        "id": department_id,
    }
