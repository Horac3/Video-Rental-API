from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
from src.film.model.film_model import FilmModel


ma = Marshmallow()
class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FilmModel
        include_relationships = True
        load_instance = True

    film_id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    description = ma.auto_field()
    release_year = ma.auto_field(required=True)
    # language_id = ma.auto_field(required=True)
    # original_language_id = ma.auto_field()
    rental_duration = ma.auto_field(required=True)
    rental_rate = ma.auto_field(required=True)
    length = ma.auto_field(required=True)
    replacement_cost = ma.auto_field(required=True)
    rating = ma.auto_field()
    special_features = ma.auto_field()
    last_update = ma.auto_field(dump_only=True)

    inventory = Nested("InventorySchema", many=True, exclude=('film',), dump_only=True)


