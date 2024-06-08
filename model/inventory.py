from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING, List
from model.base import Base
from model.film import Film
from model.rental import RentalModel




class InventoryModel(Base):
    __tablename__ = 'inventory'
    inventory_id: Mapped[int] = mapped_column(primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey('film.film_id'))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.store_id'))
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    rentals: Mapped[List["RentalModel"]] = relationship("RentalModel", back_populates="inventory")
    film: Mapped[List["Film"]] = relationship("Film", back_populates="inventory")