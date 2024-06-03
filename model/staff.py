from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from model.base import Base

if TYPE_CHECKING:
    from model.rental import Rental

class StaffModel(Base):
    __tablename__ = 'staff'
    staff_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    address_id: Mapped[int] = mapped_column(ForeignKey('address.address_id'))
    email: Mapped[str]
    store_id: Mapped[int] = mapped_column(ForeignKey('store.store_id'))
    active: Mapped[int]
    username: Mapped[str]
    password: Mapped[str]
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    rentals: Mapped[list["RentalModel"]] = relationship("RentalModel", back_populates="staff")

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        from model.rental import RentalModel
        cls.rentals = relationship("RentalModel", back_populates="staff")
