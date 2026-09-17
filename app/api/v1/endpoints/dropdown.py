from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.reference_type import ReferenceType
from app.models.reference_value import ReferenceValue
from app.schemas.reference_type import DropdownRequest
from app.schemas.reference_value import ReferenceValueRead


router = APIRouter(
    prefix="/dropdown",
    tags=["Dropdown"]
)


@router.post("/", response_model=list[ReferenceValueRead])
def get_dropdown(
    data: DropdownRequest,
    db: Session = Depends(get_db)
):
    reference_type = (
        db.query(ReferenceType)
        .filter(ReferenceType.type_name == data.reference_type)
        .first()
    )

    if not reference_type:
        raise HTTPException(
            status_code=404,
            detail="Reference type not found"
        )

    values = (
        db.query(ReferenceValue)
        .filter(
            ReferenceValue.reference_type_id == reference_type.id
        )
        .order_by(ReferenceValue.sequence_number)
        .all()
    )

    return values