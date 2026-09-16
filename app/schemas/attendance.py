from datetime import date as DateType, time as TimeType
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class AttendanceCreate(BaseModel):
    user_id: int
    date: DateType
    check_in: TimeType | None = None
    check_out: TimeType | None = None
    working_hours: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    status: AttendanceStatus


class AttendanceEdit(BaseModel):
    user_id: int | None = None
    date: DateType | None = None
    check_in: TimeType | None = None
    check_out: TimeType | None = None
    working_hours: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    status: AttendanceStatus | None = None


class AttendanceRead(BaseModel):
    id: int
    user_id: int
    date: DateType
    check_in: TimeType | None = None
    check_out: TimeType | None = None
    working_hours: Decimal | None = None
    status: AttendanceStatus

    model_config = ConfigDict(from_attributes=True)