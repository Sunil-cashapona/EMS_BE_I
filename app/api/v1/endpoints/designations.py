from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import authorization_user, get_current_user
from app.models.user import User
from app.schemas.designation import DesignationCreate, DesignationEdit, DesignationRead
from app.services.designation_service import (
    create_designation,
    get_designation_by_id,
    get_designations,
    soft_delete_designation,
    update_designation,
)


router = APIRouter()


@router.post(
    "/",
    response_model=DesignationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new designation (Admin only)",
)
def create_new_designation(
    designation_in: DesignationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return create_designation(db=db, designation_data=designation_in)


@router.get(
    "/",
    response_model=list[DesignationRead],
    status_code=status.HTTP_200_OK,
    summary="List all designations",
)
def list_designations(
    is_active: bool | None = Query(
        default=None,
        description="Filter by active status (true/false). Omit to get all.",
    ),
    search: str | None = Query(
        default=None,
        description="Search designations by name",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_designations(db=db, is_active=is_active, search=search)


@router.get(
    "/{designation_id}",
    response_model=DesignationRead,
    status_code=status.HTTP_200_OK,
    summary="Get designation by ID",
)
def get_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_designation_by_id(db=db, designation_id=designation_id)


@router.put(
    "/{designation_id}",
    response_model=DesignationRead,
    status_code=status.HTTP_200_OK,
    summary="Update a designation (Admin only)",
)
def update_existing_designation(
    designation_id: int,
    designation_in: DesignationEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return update_designation(
        db=db,
        designation_id=designation_id,
        designation_data=designation_in,
    )


@router.delete(
    "/{designation_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft delete (deactivate) a designation (Admin only)",
)
def delete_existing_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(authorization_user),
):
    return soft_delete_designation(db=db, designation_id=designation_id)
