from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class DesignationCreate(BaseModel):
    designation_name: str = Field(..., max_length=15)
    is_active: bool = True
    date_created: date | None = None


class DesignationEdit(BaseModel):
    designation_name: str | None = Field(default=None, max_length=15)
    is_active: bool | None = None
    date_created: date | None = None


class DesignationRead(BaseModel):
    id: int
    designation_name: str
    is_active: bool
    date_created: date | None = None

    model_config = ConfigDict(from_attributes=True)