from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.core.security import authorization_user
from app.models.user import User
from app.core.database import get_db

from app.schemas.directory import EmployeeDiretoryResponse
from app.services.directory import get_employee_directory

router = APIRouter(
    prefix="/directory",
    tags=["Directory"],
)

@router.get(
    "/Employee Directory",
    response_model=list[EmployeeDiretoryResponse]
)

def emplyoee_directory(
    db: Session = Depends(get_db),
    current_user = Depends(authorization_user)
):
    
    return get_employee_directory(db)