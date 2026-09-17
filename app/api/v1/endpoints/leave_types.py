from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.leave_type import LeaveType
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeEdit, LeaveTypeRead

router = APIRouter()

@router.post("/", response_model=LeaveTypeRead, status_code=status.HTTP_201_CREATED)
def create_leave_type(
    leave_type_in: LeaveTypeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = LeaveType(**leave_type_in.model_dump())
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type

@router.get("/", response_model=List[LeaveTypeRead])
def read_leave_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(LeaveType).offset(skip).limit(limit).all()

@router.get("/{leave_type_id}", response_model=LeaveTypeRead)
def read_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")
    return leave_type

@router.patch("/{leave_type_id}", response_model=LeaveTypeRead)
def update_leave_type(
    leave_type_id: int,
    leave_type_in: LeaveTypeEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")
    
    update_data = leave_type_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leave_type, field, value)
        
    db.commit()
    db.refresh(leave_type)
    return leave_type

@router.delete("/{leave_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    leave_type = db.query(LeaveType).filter(LeaveType.id == leave_type_id).first()
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")
    
    db.delete(leave_type)
    db.commit()
    return None