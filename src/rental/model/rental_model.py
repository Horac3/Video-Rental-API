from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime

from src.base import Base
from src.customer.model.customer_model import CustomerModel

from src.staff.model.staff_model import StaffModel
from src.utils.db import db
if TYPE_CHECKING:
    from src.inventory.model.inventory_model import InventoryModel

class RentalModel(db.Model):
    __tablename__ = "rental"
    rental_id: Mapped[int] = mapped_column(primary_key=True)
    rental_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventory.inventory_id'))
    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.customer_id'))
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    staff_id: Mapped[int] = mapped_column(ForeignKey('staff.staff_id'))
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer: Mapped["CustomerModel"] = relationship("CustomerModel", back_populates="rentals")
    inventory: Mapped["InventoryModel"] = relationship("InventoryModel", back_populates="rentals")
    staff: Mapped["StaffModel"] = relationship("StaffModel", back_populates="rentals")
