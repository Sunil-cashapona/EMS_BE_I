from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DepartmentCreate(BaseModel):
    dep_name: str = Field(..., min_length=1, max_length=100)
    date_created: date | None = None

    @field_validator("dep_name", mode="before")
    @classmethod
    def strip_dep_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Department name cannot be empty")
        return value


class DepartmentEdit(BaseModel):
    dep_name: str | None = Field(default=None, min_length=1, max_length=100)
    date_created: date | None = None

    @field_validator("dep_name", mode="before")
    @classmethod
    def strip_dep_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Department name cannot be empty")
        return value


class DepartmentRead(BaseModel):
    id: int
    dep_name: str
    date_created: date | None = None

    model_config = ConfigDict(from_attributes=True)