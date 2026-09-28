from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.salary_record import SalaryHistoryResponse
from app.schemas.salary_structure import CurrentSalaryStructureResponse
from app.services.salary_service import get_current_salary_structure,get_salary_history


router = APIRouter(
    prefix="/salary",
    tags=["Salary"]
)

@router.get(
    "",
    response_model=CurrentSalaryStructureResponse
)
def current_salary_structure(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_current_salary_structure(
        db=db,
        user_id=current_user.id
    )


@router.get(
    "/history",
    response_model=list[SalaryHistoryResponse]
)
def salary_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_salary_history(
        db=db,
        user_id=current_user.id
    )

