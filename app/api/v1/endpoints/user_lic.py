from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_lic import UserLic
from app.schemas.user_lic import UserLicCreate, UserLicEdit, UserLicRead

router = APIRouter()

@router.post("/", response_model=UserLicRead, status_code=status.HTTP_201_CREATED)
def create_user_lic(
    lic_in: UserLicCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    lic_entry = UserLic(**lic_in.model_dump())
    db.add(lic_entry)
    db.commit()
    db.refresh(lic_entry)
    return lic_entry

@router.get("/user/{user_id}", response_model=List[UserLicRead])
def get_user_lic_records(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(UserLic).filter(UserLic.user_id == user_id).all()

@router.get("/{lic_id}", response_model=UserLicRead)
def get_lic_record(
    lic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    lic_entry = db.query(UserLic).filter(UserLic.id == lic_id).first()
    if not lic_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LIC record not found")
    return lic_entry

@router.patch("/{lic_id}", response_model=UserLicRead)
def update_user_lic(
    lic_id: int,
    lic_in: UserLicEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    lic_entry = db.query(UserLic).filter(UserLic.id == lic_id).first()
    if not lic_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LIC record not found")
    
    update_data = lic_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lic_entry, key, value)
        
    db.commit()
    db.refresh(lic_entry)
    return lic_entry

@router.delete("/{lic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_lic(
    lic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    lic_entry = db.query(UserLic).filter(UserLic.id == lic_id).first()
    if not lic_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LIC record not found")
    
    db.delete(lic_entry)
    db.commit()
    return None