from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from sqlalchemy import literal
from src.film.model.film_model import FilmModel
from src.inventory.model.inventory_model import InventoryModel
from src.rental.model.rental_model import RentalModel
from src.utils.db import db
from src.inventory.schema.inventory_schema import InventorySchema
from sqlalchemy.orm import joinedload

blp = Blueprint("Inventory", "Inventory", description= "Inventory Endpoints")
# blp = Blueprint("inventory", "inventory", url_prefix= "/film ")

@blp.route("/inventory")
class InventoryRoute(MethodView):
    @blp.response(200, InventorySchema(many=True))
    def get(self):
            # Eagerly load related models using joinedload
            rented_and_returned = (
                db.session.query(InventoryModel)
                .join(FilmModel, FilmModel.film_id == InventoryModel.film_id)
                .join(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
                .filter(RentalModel.return_date.isnot(None))
                .options(joinedload(InventoryModel.film), joinedload(InventoryModel.rentals))
            ).all()

            never_rented = (
                db.session.query(InventoryModel)
                .outerjoin(FilmModel, FilmModel.film_id == InventoryModel.film_id)
                .outerjoin(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
                .filter(RentalModel.rental_id.is_(None))
                .options(joinedload(InventoryModel.film), joinedload(InventoryModel.rentals))
            ).all()

            # Combine the two queries
            combined_results = rented_and_returned + never_rented

            # Serialize the data using InventorySchema
            inventory_schema = InventorySchema(many=True)
            serialized_data = inventory_schema.dump(combined_results)

            return jsonify(serialized_data)