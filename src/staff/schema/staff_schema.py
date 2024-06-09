from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
from src.staff.model.staff_model import StaffModel


ma = Marshmallow()

class StaffSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StaffModel
        include_relationships = True
        load_instance = True

    staff_id = ma.auto_field(dump_only=True)
    first_name = ma.auto_field(required=True)
    last_name = ma.auto_field(required=True)
    address_id = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    store_id = ma.auto_field(required=True)
    active = ma.auto_field(required=True)
    username = ma.auto_field(required=True)
    password = ma.auto_field(load_only=True)
    last_update = ma.auto_field(dump_only=True)

    rentals = Nested("RentalSchema", many=True, exclude=('staff',), dump_only=True)


