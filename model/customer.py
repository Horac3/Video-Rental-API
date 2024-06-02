from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from model.base import Base

if TYPE_CHECKING:
    from model.rental import RentalModel

class CustomerModel(Base):
    __tablename__ = 'customer'
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey('address.address_id'))
    active: Mapped[int]
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rentals: Mapped[list["RentalModel"]] = relationship("RentalModel", back_populates="customer")

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        from model.rental import RentalModel
        cls.rentals = relationship("RentalModel", back_populates="customer")
