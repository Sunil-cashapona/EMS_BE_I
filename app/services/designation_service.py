from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.designation import Designation
from app.schemas.designation import DesignationCreate, DesignationEdit


def create_designation(
    db: Session,
    designation_data: DesignationCreate,
) -> Designation:
    normalized_name = designation_data.designation_name.strip()

    existing = (
        db.query(Designation)
        .filter(func.lower(Designation.designation_name) == normalized_name.lower())
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Designation with name '{normalized_name}' already exists",
        )

    desig_dict = designation_data.model_dump()
    if not desig_dict.get("date_created"):
        desig_dict["date_created"] = date.today()

    new_designation = Designation(**desig_dict)
    db.add(new_designation)
    db.commit()
    db.refresh(new_designation)
    return new_designation


def get_designations(
    db: Session,
    is_active: bool | None = None,
    search: str | None = None,
) -> list[Designation]:
    query = db.query(Designation)

    if is_active is not None:
        query = query.filter(Designation.is_active == is_active)

    if search:
        query = query.filter(Designation.designation_name.ilike(f"%{search.strip()}%"))

    return query.order_by(Designation.id.asc()).all()


def get_designation_by_id(db: Session, designation_id: int) -> Designation:
    designation = (
        db.query(Designation)
        .filter(Designation.id == designation_id)
        .first()
    )
    if not designation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Designation with id {designation_id} not found",
        )
    return designation


def update_designation(
    db: Session,
    designation_id: int,
    designation_data: DesignationEdit,
) -> Designation:
    designation = get_designation_by_id(db, designation_id)

    update_dict = designation_data.model_dump(exclude_unset=True)

    if "designation_name" in update_dict and update_dict["designation_name"]:
        normalized_name = update_dict["designation_name"].strip()
        existing = (
            db.query(Designation)
            .filter(
                func.lower(Designation.designation_name) == normalized_name.lower(),
                Designation.id != designation_id,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Designation with name '{normalized_name}' already exists",
            )
        update_dict["designation_name"] = normalized_name

    for field, value in update_dict.items():
        setattr(designation, field, value)

    db.commit()
    db.refresh(designation)
    return designation


def soft_delete_designation(db: Session, designation_id: int) -> dict:
    designation = get_designation_by_id(db, designation_id)

    designation.is_active = False
    db.commit()
    db.refresh(designation)

    return {
        "message": "Designation deactivated successfully",
        "id": designation_id,
        "is_active": designation.is_active,
    }
