from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from flask_marshmallow import Marshmallow
from src.customer.model.customer_model import CustomerModel



ma = Marshmallow()


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        include_relationships = True
        load_instance = True

    customer_id = ma.auto_field(dump_only=True)
    first_name = ma.auto_field(required=True)
    last_name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    # address_id = ma.auto_field(required=True)
    active = ma.auto_field(required=True)
    create_date = ma.auto_field(dump_only=True)
    last_update = ma.auto_field(dump_only=True)

    rentals = Nested("RentalSchema", many=True, exclude=('customer',), dump_only=True)


