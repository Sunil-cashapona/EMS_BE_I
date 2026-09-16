from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.reference_type import ReferenceType
from app.models.reference_value import ReferenceValue
from app.schemas.reference_type import ReferenceTypeCreate, ReferenceTypeRead
from app.schemas.reference_value import ReferenceValueCreate, ReferenceValueRead

router = APIRouter()

# Reference Types
@router.post("/types", response_model=ReferenceTypeRead, status_code=status.HTTP_201_CREATED)
def create_reference_type(
    ref_type_in: ReferenceTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ref_type = ReferenceType(**ref_type_in.model_dump())
    db.add(ref_type)
    db.commit()
    db.refresh(ref_type)
    return ref_type

@router.get("/types", response_model=List[ReferenceTypeRead])
def read_reference_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(ReferenceType).offset(skip).limit(limit).all()

# Reference Values
@router.post("/values", response_model=ReferenceValueRead, status_code=status.HTTP_201_CREATED)
def create_reference_value(
    ref_val_in: ReferenceValueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ref_val = ReferenceValue(**ref_val_in.model_dump())
    db.add(ref_val)
    db.commit()
    db.refresh(ref_val)
    return ref_val

@router.get("/values/{type_code}", response_model=List[ReferenceValueRead])
def get_values_by_type(
    type_code: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    ref_type = db.query(ReferenceType).filter(ReferenceType.code == type_code).first()
    if not ref_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reference type not found")
    return db.query(ReferenceValue).filter(ReferenceValue.reference_type_id == ref_type.id).all()