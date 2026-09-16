from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.departments import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentEdit,
    DepartmentRead,
)


router = APIRouter()


# 1. Create
@router.post("/",response_model=DepartmentRead,status_code=status.HTTP_201_CREATED,)
def create_department(
    dept_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing_dept = (
        db.query(Department)
        .filter(Department.dep_name == dept_in.dep_name)
        .first()
    )

    if existing_dept:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department with this name already exists",
        )

    dept = Department(dep_name=dept_in.dep_name)

    db.add(dept)
    db.commit()
    db.refresh(dept)

    return dept


# 2. Read All
@router.get("/", response_model=List[DepartmentRead])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Department).offset(skip).limit(limit).all()


# 3. Read Single
@router.get("/{dept_id}", response_model=DepartmentRead)
def read_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    dept = (
        db.query(Department)
        .filter(Department.id == dept_id)
        .first()
    )

    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    return dept


# 4. Update
@router.patch("/{dept_id}", response_model=DepartmentRead)
def update_department(
    dept_id: int,
    dept_in: DepartmentEdit,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    dept = (
        db.query(Department)
        .filter(Department.id == dept_id)
        .first()
    )

    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    update_data = dept_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(dept, field, value)

    db.commit()
    db.refresh(dept)

    return dept


# 5. Delete
@router.delete("/{dept_id}",status_code=status.HTTP_204_NO_CONTENT,)
def delete_department(
    dept_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    dept = (
        db.query(Department)
        .filter(Department.id == dept_id)
        .first()
    )

    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    db.delete(dept)
    db.commit()

    return None