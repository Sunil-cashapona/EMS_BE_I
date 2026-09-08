from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    dep_name: str = Field(..., max_length=100)
    date_created: date | None = None


class DepartmentEdit(BaseModel):
    dep_name: str | None = Field(default=None, max_length=100)
    date_created: date | None = None


class DepartmentRead(BaseModel):
    id: int
    dep_name: str
    date_created: date | None = None

    model_config = ConfigDict(from_attributes=True)