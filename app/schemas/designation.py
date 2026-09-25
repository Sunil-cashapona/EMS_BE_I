from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DesignationCreate(BaseModel):
    designation_name: str = Field(..., min_length=1, max_length=15)
    is_active: bool = True
    date_created: date | None = None

    @field_validator("designation_name", mode="before")
    @classmethod
    def strip_designation_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Designation name cannot be empty")
        return value


class DesignationEdit(BaseModel):
    designation_name: str | None = Field(default=None, min_length=1, max_length=15)
    is_active: bool | None = None
    date_created: date | None = None

    @field_validator("designation_name", mode="before")
    @classmethod
    def strip_designation_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Designation name cannot be empty")
        return value


class DesignationRead(BaseModel):
    id: int
    designation_name: str
    is_active: bool
    date_created: date | None = None

    model_config = ConfigDict(from_attributes=True)