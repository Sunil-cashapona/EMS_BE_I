from pydantic import BaseModel, ConfigDict, Field


class LeaveTypeCreate(BaseModel):
    type_name: str = Field(..., max_length=50)
    max_days_per_year: int


class LeaveTypeEdit(BaseModel):
    type_name: str | None = Field(default=None, max_length=50)
    max_days_per_year: int | None = None


class LeaveTypeRead(BaseModel):
    id: int
    type_name: str
    max_days_per_year: int

    model_config = ConfigDict(from_attributes=True)