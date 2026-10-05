from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.holiday import Holiday, HolidayType
from app.schemas.holiday import HolidayCreate


def create_holiday(
    db: Session,
    request: HolidayCreate
):

    existing_holiday = (
        db.query(Holiday)
        .filter(
            Holiday.date == request.date
        )
        .first()
    )

    if existing_holiday:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Holiday already exists for this date"
        )

    try:
        holiday_type = HolidayType(request.holiday_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid holiday type"
        )

    holiday = Holiday(
        holiday_name=request.holiday_name.strip(),
        date=request.date,
        day=request.date.strftime("%A"),
        holiday_type=holiday_type
    )

    db.add(holiday)
    db.commit()
    db.refresh(holiday)

    return holiday


def get_holidays(
    db: Session,
    year: int | None = None
):

    query = db.query(Holiday)

    if year:
        query = query.filter(
            Holiday.date >= f"{year}-01-01",
            Holiday.date <= f"{year}-12-31"
        )

    return (
        query
        .order_by(Holiday.date.asc())
        .all()
    )