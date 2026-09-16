from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.file import File as FileModel
from app.schemas.user_file import UserFileRead

router = APIRouter()

@router.post("/upload", response_model=UserFileRead, status_code=status.HTTP_201_CREATED)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Save file to storage disk/cloud, then record metadata in DB
    db_file = FileModel(
        filename=file.filename,
        content_type=file.content_type,
        user_id=current_user.id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.get("/user/{user_id}", response_model=List[UserFileRead])
def list_user_files(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(FileModel).filter(FileModel.user_id == user_id).all()