from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from sqlalchemy import literal
from src.film.model.film_model import FilmModel
from src.inventory.model.inventory_model import InventoryModel
from src.rental.model.rental_model import RentalModel
from src.utils.db import db
from src.inventory.schema.inventory_schema import InventorySchema

blp = Blueprint("Inventory", "Inventory", description= "Inventory Endpoints")
# blp = Blueprint("inventory", "inventory", url_prefix= "/film ")

@blp.route("/inventory")
class InventoryRoute(MethodView):
    @blp.response(200, InventorySchema(many=True))
    def get(self ):
    # -- Films that have been rented and returned
        # SELECT
        #     f.film_id,
        #     f.title,
        #     'Rented and Returned' AS status
        # FROM
        #     film f
        # JOIN
        #     inventory i ON f.film_id = i.film_id
        # JOIN
        #     rental r ON i.inventory_id = r.inventory_id
        # WHERE
        #     r.return_date IS NOT NULL

        # UNION

        # -- Films that have never been rented out
        # SELECT
        #     f.film_id,
        #     f.title,
        #     'Never Rented' AS status
        # FROM
        #     film f
        # LEFT JOIN
        #     inventory i ON f.film_id = i.film_id
        # LEFT JOIN
        #     rental r ON i.inventory_id = r.inventory_id
        # WHERE
        #     r.rental_id IS NULL;
        rented_and_returned = (
        db.session.query(
            InventoryModel.inventory_id,
            FilmModel.film_id,
            FilmModel.title,
            literal('Rented and Returned').label('status')
        )
        .join(InventoryModel, FilmModel.film_id == InventoryModel.film_id)
        .join(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
        .filter(RentalModel.return_date.isnot(None))
    )


        # Query for films that have never been rented out
        never_rented = (
        db.session.query(
            InventoryModel.inventory_id,
            FilmModel.film_id,
            FilmModel.title,
            literal('Never Rented').label('status')
        )
        .outerjoin(InventoryModel, FilmModel.film_id == InventoryModel.film_id)
        .outerjoin(RentalModel, InventoryModel.inventory_id == RentalModel.inventory_id)
        .filter(RentalModel.rental_id.is_(None))
    )

        # Combine the two queries using union_all
        combined_query = rented_and_returned.union_all(never_rented)
        results = db.session.execute(combined_query).fetchall()

        # Convert results to a dictionary
        films_dict = []
        for result in results:
            films_dict.append({
                'inventory_id': result[0],
                'film_id': result[1],
                'title': result[2],
                'status': result[3]
            })
        return films_dict
