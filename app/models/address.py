from sqlalchemy import  ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.core.database import Base


class Address(Base):

    __tablename__ = "mst_address"
    __table_args__ = {"schema": "EMS_DB"}  

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    address: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("EMS_DB.txn_user.id") ,       
        nullable=False
    )
 

    city: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    pincode: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    user = relationship("User", back_populates="address")

   
