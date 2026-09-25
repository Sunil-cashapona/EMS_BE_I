from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import authorization_user, get_current_user
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentEdit, DepartmentRead
from app.services.department_service import (
    create_department,
    delete_department,
    get_department_by_id,
    get_departments,
    update_department,
)


router = APIRouter()


@router.post(
    "/",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new department (Admin only)",
)
def create_new_department(
    department_in: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return create_department(db=db, department_data=department_in)


@router.get(
    "/",
    response_model=list[DepartmentRead],
    status_code=status.HTTP_200_OK,
    summary="List all departments",
)
def list_departments(
    search: str | None = Query(default=None, description="Search departments by name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_departments(db=db, search=search)


@router.get(
    "/{department_id}",
    response_model=DepartmentRead,
    status_code=status.HTTP_200_OK,
    summary="Get department by ID",
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_department_by_id(db=db, department_id=department_id)


@router.put(
    "/{department_id}",
    response_model=DepartmentRead,
    status_code=status.HTTP_200_OK,
    summary="Update a department (Admin only)",
)
def update_existing_department(
    department_id: int,
    department_in: DepartmentEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return update_department(
        db=db,
        department_id=department_id,
        department_data=department_in,
    )


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a department (Admin only)",
)
def delete_existing_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return delete_department(db=db, department_id=department_id)
