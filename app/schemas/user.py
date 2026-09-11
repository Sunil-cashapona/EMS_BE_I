from datetime import date, datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.models.user import Gender, Role, EmploymentType

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)
    
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value:EmailStr) ->EmailStr:
        return str(value).strip().lower()
    
class LoginUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str


class LoginResponse(BaseModel):
    user: LoginUser
    access_token: str
    refresh_token: str
    token_type: str
    
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
    created_at: datetime
    updated_at: datetime
    #last_login: datetime | None = None

    address: str
    employee_id: str = Field(..., max_length=30)
    joining_date: date
    employment_type: EmploymentType

    emergency_contact: str = Field(..., max_length=20)
    blood_group: str | None = Field(default=None, max_length=10)
    salary:  float | None = None
    lic_policy_number: str |None=None

    @field_validator(
        "first_name",
        "last_name",
        "address",
        "employee_id",
        "phonenumber",
        "emergency_contact",
        "blood_group",
        mode="before"
    )
    @classmethod
    def strip_string_values(cls, value):
        if value is None:
            return value

        if isinstance(value, str):
            value = value.strip()

        return value
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> EmailStr:
        return str(value).strip().lower()
    
    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Date of birth must be in the past")

        return value
    
    @field_validator("joining_date")
    @classmethod
    def validate_joining_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Joining date cannot be in the future")

        return value
    
    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Employee ID cannot be empty")

        return value
    
    @field_validator("phonenumber", "emergency_contact")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        digits = "".join(char for char in value if char.isdigit())

        if len(digits) < 7:
            raise ValueError("Phone number must contain at least 7 digits")

        if len(digits) > 15:
            raise ValueError("Phone number cannot contain more than 15 digits")

        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot be empty")
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any (char.isupper() for char in value):
            raise ValueError ("Password must contain at least one uppercase letter")
        if not any(char.isalnum() for char in value):
            raise ValueError ("Password must contain atleast one special character")

        return value
    
    
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
    employee_id: str | None = Field(default=None, max_length=30)
    joining_date: date | None = None
    employment_type: EmploymentType | None = None

    emergency_contact: str | None = Field(default=None, max_length=20)
    blood_group: str | None = Field(default=None, max_length=10)

    
    @field_validator(
        "first_name",
        "last_name",
        "address",
        "employee_id",
        "phonenumber",
        "emergency_contact",
        "blood_group",
        mode="before",
    )
    @classmethod
    def strip_string_values(cls, value):
        if value is None:
            return value

        if isinstance(value, str):
            value = value.strip()

        return value


    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> EmailStr:
        # sourcery skip: assign-if-exp, reintroduce-else
        if value is None:
            return value

        return str(value).strip().lower()


    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value: date | None) -> date | None:
        if value is None:
            return value

        if value >= date.today():
            raise ValueError("Date of birth must be in the past")

        return value

    @field_validator("joining_date")
    @classmethod
    def validate_joining_date(cls, value: date | None) -> date | None:
        if value is None:
            return value

        if value > date.today():
            raise ValueError("Joining date cannot be in the future")

        return value



    @field_validator("phonenumber", "emergency_contact")
    @classmethod
    def validate_phone_number(cls, value: str | None) -> str | None:
        if value is None:
            return value

        digits = "".join(char for char in value if char.isdigit())

        if len(digits) < 7:
            raise ValueError("Phone number must contain at least 7 digits")

        if len(digits) > 15:
            raise ValueError("Phone number cannot contain more than 15 digits")

        return value


    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str | None) -> str | None:
        if value is None:
            return value

        if not value.strip():
            raise ValueError("Password cannot be empty")

        return value



class UserResponse(BaseModel):
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
    employee_id: str
    joining_date: date
    employment_type: EmploymentType
    salary: float | None = None
    lic_policy_number: str | None = None

    emergency_contact: str
    blood_group: str | None = None

    last_login: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)