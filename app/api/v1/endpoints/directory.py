from fastapi import APIRouter , Depends
from sqlalchemy.orm import Query, Session
from app.core.security import authorization_user
from app.models.user import User
from app.core.database import get_db
from fastapi import APIRouter, Depends, Query
from app.schemas.directory import EmployeeDirectoryResponse, EmployeeDirectoryPaginationResponse
from app.services.directory import get_employee_directory

router = APIRouter(
    prefix="/directory",
    tags=["Directory"],
)

@router.get(
    "/Employee Directory",
    response_model=EmployeeDirectoryPaginationResponse
)

def emplyoee_directory(
    db: Session = Depends(get_db),
    current_user = Depends(authorization_user),
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=10, ge=1, description="Page size"),
    search: str | None = Query(None, description="Search by name , email or employee id"),
    dep_id: int | None = Query(None, description="Department Filter"),



):

    
    
    return get_employee_directory(
        db=db,
        page=page,
        size=size,
        search=search,
        dep_id=dep_id,
    )