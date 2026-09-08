from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserFileCreate(BaseModel):
    user_id: int
    document_type: str = Field(..., max_length=50)
    file_path: str = Field(..., max_length=255)
    uploaded_time: datetime | None = None


class UserFileEdit(BaseModel):
    user_id: int | None = None
    document_type: str | None = Field(default=None, max_length=50)
    file_path: str | None = Field(default=None, max_length=255)
    uploaded_time: datetime | None = None


class UserFileRead(BaseModel):
    id: int
    user_id: int
    document_type: str
    file_path: str
    uploaded_time: datetime

    model_config = ConfigDict(from_attributes=True)