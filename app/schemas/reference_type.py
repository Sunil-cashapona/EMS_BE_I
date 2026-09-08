from pydantic import BaseModel, ConfigDict, Field


class ReferenceTypeCreate(BaseModel):
    type_name: str = Field(..., max_length=100)


class ReferenceTypeEdit(BaseModel):
    type_name: str | None = Field(default=None, max_length=100)


class ReferenceTypeRead(BaseModel):
    id: int
    type_name: str

    model_config = ConfigDict(from_attributes=True)