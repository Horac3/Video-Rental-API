from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
from src.inventory.model.inventory_model import InventoryModel


ma = Marshmallow()
class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryModel
        include_relationships = True
        load_instance = True

    inventory_id = ma.auto_field(dump_only=True)
    # film_id = ma.auto_field(dump_only=True)
    # store_id = ma.auto_field(dump_only=True)
    last_update = ma.auto_field(dump_only=True)

    # rentals = Nested("RentalSchema", many=True, exclude=('inventory',), dump_only=True)
    # film = Nested("FilmSchema", many=True, exclude=('inventory',), dump_only=True)
