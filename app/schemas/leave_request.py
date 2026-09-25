from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveRequestCreate(BaseModel):
    user_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str | None = None
    status: LeaveStatus = LeaveStatus.PENDING
    approved: int | None = None
    applied_at: datetime | None = None


class LeaveRequestEdit(BaseModel):
    user_id: int | None = None
    leave_type_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = None
    status: LeaveStatus | None = None
    approved: int | None = None
    applied_at: datetime | None = None


class LeaveRequestRead(BaseModel):
    id: int
    user_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str | None = None
    status: LeaveStatus
    approved: int | None = None
    applied_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LeaveApplyRequest(BaseModel):
    leave_type_id: int

    start_date: date

    end_date: date

    reason: str = Field(
        ...,
        min_length=3,
        max_length=500
    )

class LeaveBalanceResponse(BaseModel):
    leave_type_id: int

    leave_type_name: str

    total_days: int

    used_days: int

    remaining_days: int

class AdminLeaveRequestRead(BaseModel):
    id: int

    user_id: int

    employee_name: str

    department: str | None = None

    leave_type_id: int

    leave_type: str

    start_date: date

    end_date: date

    number_of_days: int

    reason: str | None = None

    status: LeaveStatus

    approved: int | None = None

    applied_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )