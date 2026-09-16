from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.attendence import Attendence
from app.models.user import User
from app.schemas.attendence import AttendanceCreate, AttendanceEdit, AttendanceRead

router = APIRouter()

@router.post("/check-in", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
def check_in(
    attendance_in: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    attendance = Attendence(**attendance_in.model_dump(), user_id=current_user.id)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@router.get("/", response_model=List[AttendanceRead])
def read_attendance_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if getattr(current_user, "role", None) == "admin":
        return db.query(Attendence).offset(skip).limit(limit).all()
    return db.query(Attendence).filter(Attendence.user_id == current_user.id).offset(skip).limit(limit).all()

@router.patch("/{attendance_id}/check-out", response_model=AttendanceRead)
def check_out(
    attendance_id: int,
    attendance_in: AttendanceEdit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(Attendence).filter(Attendence.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
        
    update_data = attendance_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)
        
    db.commit()
    db.refresh(record)
    return record