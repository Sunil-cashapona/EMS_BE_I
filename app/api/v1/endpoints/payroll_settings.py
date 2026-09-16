from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.payroll_settings import PayrollSettings
from app.schemas.payroll_settings import PayrollSettingsCreate, PayrollSettingsEdit, PayrollSettingsRead

router = APIRouter()

@router.post("/", response_model=PayrollSettingsRead, status_code=status.HTTP_201_CREATED)
def create_payroll_settings(
    settings_in: PayrollSettingsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    settings = PayrollSettings(**settings_in.model_dump())
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/", response_model=List[PayrollSettingsRead])
def read_payroll_settings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(PayrollSettings).offset(skip).limit(limit).all()

@router.patch("/{setting_id}", response_model=PayrollSettingsRead)
def update_payroll_settings(
    setting_id: int,
    settings_in: PayrollSettingsEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    setting = db.query(PayrollSettings).filter(PayrollSettings.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    
    update_data = settings_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(setting, field, value)
        
    db.commit()
    db.refresh(setting)
    return setting