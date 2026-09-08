from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class UserLICCreate(BaseModel):
    user_id: int
    policy_number: str = Field(..., max_length=50)
    provider: str = Field(..., max_length=100)
    due_date: date


class UserLICEdit(BaseModel):
    user_id: int | None = None
    policy_number: str | None = Field(default=None, max_length=50)
    provider: str | None = Field(default=None, max_length=100)
    due_date: date | None = None


class UserLICRead(BaseModel):
    id: int
    user_id: int
    policy_number: str
    provider: str
    due_date: date

    model_config = ConfigDict(from_attributes=True)