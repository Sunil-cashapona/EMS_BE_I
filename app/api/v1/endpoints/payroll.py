from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.salary_structure import SalaryStructure
from app.models.salary_record import SalaryRecord
from app.schemas.salary_stucture import SalaryStructureCreate, SalaryStructureRead
from app.schemas.salary_recod import SalaryRecordCreate, SalaryRecordRead

router = APIRouter()

# Salary Structure
@router.post("/structures", response_model=SalaryStructureRead, status_code=status.HTTP_201_CREATED)
def assign_salary_structure(
    structure_in: SalaryStructureCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    structure = SalaryStructure(**structure_in.model_dump())
    db.add(structure)
    db.commit()
    db.refresh(structure)
    return structure

@router.get("/structures/user/{user_id}", response_model=SalaryStructureRead)
def get_user_salary_structure(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    structure = db.query(SalaryStructure).filter(SalaryStructure.user_id == user_id).first()
    if not structure:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Salary structure not found")
    return structure

# Salary Records (Payslips)
@router.post("/records", response_model=SalaryRecordRead, status_code=status.HTTP_201_CREATED)
def create_salary_record(
    record_in: SalaryRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    record = SalaryRecord(**record_in.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/records/user/{user_id}", response_model=List[SalaryRecordRead])
def get_user_salary_records(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(SalaryRecord).filter(SalaryRecord.user_id == user_id).all()