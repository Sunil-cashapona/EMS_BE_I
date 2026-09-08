from datetime import date as DateType

from pydantic import BaseModel, ConfigDict, Field


class HolidayCreate(BaseModel):
    holiday_name: str = Field(..., max_length=100)
    date: DateType


class HolidayEdit(BaseModel):
    holiday_name: str | None = Field(default=None, max_length=100)
    date: DateType | None = None


class HolidayRead(BaseModel):
    id: int
    holiday_name: str
    date: DateType

    model_config = ConfigDict(from_attributes=True)