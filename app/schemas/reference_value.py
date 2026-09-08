from pydantic import BaseModel, ConfigDict, Field


class ReferenceValueCreate(BaseModel):
    reference_type_id: int
    reference_value: str = Field(..., max_length=100)
    sequence_number: int


class ReferenceValueEdit(BaseModel):
    reference_type_id: int | None = None
    reference_value: str | None = Field(default=None, max_length=100)
    sequence_number: int | None = None


class ReferenceValueRead(BaseModel):
    id: int
    reference_type_id: int
    reference_value: str
    sequence_number: int

    model_config = ConfigDict(from_attributes=True)