from datetime import date, datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Gender(str, PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Role(str, PyEnum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class EmploymentType(str, PyEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"


class User(Base):

    __tablename__ = "txn_user"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    dob: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    gender: Mapped[Gender | None] = mapped_column(
        Enum(Gender),
        nullable=True
    )

    phonenumber: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    dep_id: Mapped[int | None] = mapped_column(
        ForeignKey("mst_department.id"),
        nullable=True
    )

    designation_id: Mapped[int | None] = mapped_column(
        ForeignKey("mst_designation.id"),
        nullable=True
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    employee_code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType),
        nullable=False
    )

    emergency_contact: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    blood_group: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    department = relationship(
        "Department"
    )

    designation = relationship(
        "Designation"
    )
