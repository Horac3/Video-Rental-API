from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING, List
from src.base import Base
from src.film.model.film_model import FilmModel
from src.rental.model.rental_model import RentalModel
from src.utils.db import db


class InventoryModel(db.Model):
    __tablename__ = 'inventory'
    inventory_id: Mapped[int] = mapped_column(primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey('film.film_id'))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.store_id'), nullable=True)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    rentals: Mapped[List["RentalModel"]] = relationship("RentalModel", back_populates="inventory")
    film: Mapped[List["FilmModel"]] = relationship("FilmModel", back_populates="inventory")