from math import ceil
from flask import jsonify, request, url_for
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
        page = request.args.get('page', 1, type=int)
        per_page = 30
        offset = (page - 1) * per_page

        # Eagerly load related models using joinedload
        rented_and_returned = (
            db.session.query(InventoryModel)
            .join(FilmModel, FilmModel.film_id == InventoryModel.film_id)
            .join(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
            .filter(RentalModel.return_date.isnot(None))
            .options(joinedload(InventoryModel.film), joinedload(InventoryModel.rentals))
            .all()
        )

        never_rented = (
            db.session.query(InventoryModel)
            .outerjoin(FilmModel, FilmModel.film_id == InventoryModel.film_id)
            .outerjoin(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
            .filter(RentalModel.rental_id.is_(None))
            .options(joinedload(InventoryModel.film), joinedload(InventoryModel.rentals))
            .all()
        )

        # Combine the two queries
        combined_results = rented_and_returned + never_rented

        # Calculate pagination details
        total = len(combined_results)
        total_pages = ceil(total / per_page)
        first_page = 1
        last_page = total_pages
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None

        # Paginate the combined results
        paginated_results = combined_results[offset:offset + per_page]

        # Serialize the data using InventorySchema
        inventory_schema = InventorySchema(many=True)
        serialized_data = inventory_schema.dump(paginated_results)

        # Generate pagination URLs
        base_url = request.base_url
        previous_page_url = url_for(request.endpoint, page=previous_page, _external=True) if previous_page else None
        next_page_url = url_for(request.endpoint, page=next_page, _external=True) if next_page else None

        # Construct pagination metadata
        pagination_metadata = {
            "total": total,
            "total_pages": total_pages,
            "first_page": url_for(request.endpoint, page=first_page, _external=True),
            "last_page": url_for(request.endpoint, page=last_page, _external=True),
            "page": page,
            "previous_page": previous_page_url,
            "next_page": next_page_url,
        }

        response = {
            "data": serialized_data,
            "pagination": pagination_metadata
        }

        return jsonify(response)