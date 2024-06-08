from typing import List, Set
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, DateTime, Numeric, SmallInteger, String, Text
from datetime import datetime
from model.base import Base


# film_id smallint UN AI PK
# title varchar(128)
# description text
# release_year year
# language_id tinyint UN
# original_language_id tinyint UN
# rental_duration tinyint UN
# rental_rate decimal(4,2)
# length smallint UN
# replacement_cost decimal(5,2)
# rating enum('G','PG','PG-13','R','NC-17')
# special_features set('Trailers','Commentaries','Deleted Scenes','Behind the Scenes')
# last_update timestamp


class Film(Base):
    __tablename__ = 'film'
    film_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    release_year: Mapped[int] = mapped_column(DateTime)
    language_id: Mapped[int] = mapped_column(ForeignKey('language.language_id'))
    original_language_id: Mapped[int] = mapped_column(ForeignKey('language.language_id'), nullable=True)
    rental_duration: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    rental_rate: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    length: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    replacement_cost: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    rating: Mapped[str] = mapped_column(Enum('G', 'PG', 'PG-13', 'R', 'NC-17'))
    special_features: Mapped[str] = mapped_column(Enum('Trailers', 'Commentaries', 'Deleted Scenes', 'Behind the Scenes'))
    last_update: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)

    inventory : Mapped[List["InventoryModel"]] = relationship("InventoryModel", back_populates="film")



