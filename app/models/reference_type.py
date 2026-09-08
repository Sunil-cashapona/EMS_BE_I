from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReferenceType(Base):

    __tablename__ = "mst_reference_type"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    type_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    values = relationship(
        "ReferenceValue",
        back_populates="reference_type"
    )
