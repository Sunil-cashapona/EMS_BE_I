from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.designation import Designation
from app.schemas.designation import DesignationCreate, DesignationEdit, DesignationRead

router = APIRouter()

@router.post("/", response_model=DesignationRead, status_code=status.HTTP_201_CREATED)
def create_designation(
    desig_in: DesignationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    desig = Designation(**desig_in.model_dump())
    db.add(desig)
    db.commit()
    db.refresh(desig)
    return desig

@router.get("/", response_model=List[DesignationRead])
def read_designations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Designation).offset(skip).limit(limit).all()

@router.get("/{designation_id}", response_model=DesignationRead)
def read_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    desig = db.query(Designation).filter(Designation.id == designation_id).first()
    if not desig:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Designation not found")
    return desig

@router.patch("/{designation_id}", response_model=DesignationRead)
def update_designation(
    designation_id: int,
    desig_in: DesignationEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    desig = db.query(Designation).filter(Designation.id == designation_id).first()
    if not desig:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Designation not found")
    
    update_data = desig_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(desig, field, value)
        
    db.commit()
    db.refresh(desig)
    return desig

@router.delete("/{designation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_designation(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    desig = db.query(Designation).filter(Designation.id == designation_id).first()
    if not desig:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Designation not found")
    
    db.delete(desig)
    db.commit()
    return None