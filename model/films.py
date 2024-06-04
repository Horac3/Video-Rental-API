from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING, List
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
    title: Mapped[str]
    description: Mapped[str]
    release_year: Mapped[datetime] = mapped_column(DateTime)
    language_id: Mapped[int] = mapped_column(ForeignKey('language.language.id'))
    original_language_id: Mapped[int] = mapped_column(ForeignKey('language.language_id'), nullable=True)



