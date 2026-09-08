from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Role(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"



class UserCreate(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    dob: date
    gender: Gender | None = None
    phonenumber: str = Field(..., max_length=20)
    email: EmailStr
    password: str
    role: Role = Role.EMPLOYEE
    is_active: bool = True

    dep_id: int | None = None
    designation_id: int | None = None

    address: str
    employee_code: str = Field(..., max_length=30)
    joining_date: date
    employment_type: EmploymentType

    emergency_contact: str = Field(..., max_length=20)
    blood_group: str | None = Field(default=None, max_length=10)


class UserEdit(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    dob: date | None = None
    gender: Gender | None = None
    phonenumber: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    password: str | None = None

    role: Role | None = None
    is_active: bool | None = None

    dep_id: int | None = None
    designation_id: int | None = None

    address: str | None = None
    employee_code: str | None = Field(default=None, max_length=30)
    joining_date: date | None = None
    employment_type: EmploymentType | None = None

    emergency_contact: str | None = Field(default=None, max_length=20)
    blood_group: str | None = Field(default=None, max_length=10)



class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    dob: date
    gender: Gender | None = None
    phonenumber: str
    email: EmailStr
    role: Role
    is_active: bool

    dep_id: int | None = None
    designation_id: int | None = None

    address: str
    employee_code: str
    joining_date: date
    employment_type: EmploymentType

    emergency_contact: str
    blood_group: str | None = None

    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)