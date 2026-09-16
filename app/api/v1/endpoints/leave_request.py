from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.leave_request import LeaveRequest
from app.models.user import User
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestEdit, LeaveRequestRead

router = APIRouter()

@router.post("/", response_model=LeaveRequestRead, status_code=status.HTTP_201_CREATED)
def apply_leave(
    leave_in: LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = LeaveRequest(**leave_in.model_dump(), user_id=current_user.id)
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave

@router.get("/", response_model=List[LeaveRequestRead])
def read_leaves(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If standard user, only list their own leaves; if admin/manager, list all
    if getattr(current_user, "role", None) == "admin":
        return db.query(LeaveRequest).offset(skip).limit(limit).all()
    return db.query(LeaveRequest).filter(LeaveRequest.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/{leave_id}", response_model=LeaveRequestRead)
def read_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    return leave

@router.patch("/{leave_id}", response_model=LeaveRequestRead)
def update_leave_status(
    leave_id: int,
    leave_in: LeaveRequestEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    
    update_data = leave_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leave, field, value)
        
    db.commit()
    db.refresh(leave)
    return leave