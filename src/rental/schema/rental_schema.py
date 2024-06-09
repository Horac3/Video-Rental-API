from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from src.customer.schema.customer_schema import CustomerSchema
from src.film.model.film_model import FilmModel
from src.inventory.schema.inventory_schema import InventorySchema
from src.staff.schema.staff_schema import StaffSchema

ma = Marshmallow()

class RentalSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FilmModel
        include_relationships = True
        load_instance = True

    rental_id = ma.auto_field(dump_only=True)
    rental_date = ma.auto_field(default=datetime.now)
    inventory_id = ma.auto_field(required=True)
    customer_id = ma.auto_field(required=True)
    return_date = ma.auto_field(default=None)
    staff_id = ma.auto_field(required=True)
    last_update = ma.auto_field(default=datetime.now)

    customer = Nested(CustomerSchema, many=True, exclude=('rental'), dump_only=True)
    inventory = Nested(InventorySchema, many=True, exclude=('rental'), dump_only=True)
    staff = Nested(StaffSchema, many=True, exclude=('rental'), dump_only=True)
