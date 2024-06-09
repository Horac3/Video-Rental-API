from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING

from src.base import Base
from src.utils.db import db

if TYPE_CHECKING:
    from src.rental.model.rental_model import RentalModel

class CustomerModel(db.Model):
    __tablename__ = 'customer'
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    address_id: Mapped[int] = mapped_column(ForeignKey('address.address_id'))
    active: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.utcnow)

    rentals: Mapped[list["RentalModel"]] = relationship("RentalModel", back_populates="customer")

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        from src.rental.model.rental_model import RentalModel
        cls.rentals = relationship("Rental", back_populates="customer")
