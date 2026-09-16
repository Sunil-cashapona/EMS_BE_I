from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.holiday import Holiday
from app.schemas.holiday import HolidayCreate, HolidayEdit, HolidayRead

router = APIRouter()

@router.post("/", response_model=HolidayRead, status_code=status.HTTP_201_CREATED)
def create_holiday(
    holiday_in: HolidayCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    holiday = Holiday(**holiday_in.model_dump())
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return holiday

@router.get("/", response_model=List[HolidayRead])
def read_holidays(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Holiday).offset(skip).limit(limit).all()

@router.get("/{holiday_id}", response_model=HolidayRead)
def read_holiday(
    holiday_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")
    return holiday

@router.patch("/{holiday_id}", response_model=HolidayRead)
def update_holiday(
    holiday_id: int,
    holiday_in: HolidayEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")
    
    update_data = holiday_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(holiday, field, value)
        
    db.commit()
    db.refresh(holiday)
    return holiday

@router.delete("/{holiday_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holiday(
    holiday_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    holiday = db.query(Holiday).filter(Holiday.id == holiday_id).first()
    if not holiday:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Holiday not found")
    
    db.delete(holiday)
    db.commit()
    return None