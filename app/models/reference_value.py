from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReferenceValue(Base):

    __tablename__ = "mst_reference_value"
    __table_args__ = {"schema": "EMS_DB"}

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    reference_type_id: Mapped[int] = mapped_column(
        ForeignKey("EMS_DB.mst_reference_type.id"),
        nullable=False
    )

    reference_value: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    reference_type = relationship(
        "ReferenceType",
        back_populates="values"
    )
