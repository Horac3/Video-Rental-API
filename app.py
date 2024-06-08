# To connect, you need SQLAlchemy engine
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker, aliased
from model.film import Film
from model.inventory import InventoryModel
from model.rental import RentalModel
from sqlalchemy.sql import func

engine = create_engine("mysql://root:121096@localhost/sakila")
try:
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print("Error occurred:", e)

session = Session(engine)

film = aliased(Film)
rental = aliased(RentalModel)
inventory = aliased(InventoryModel)

# stmt = select(InventoryModel)
# results = session.query(InventoryModel).distinct()
# for result in results:
#     print(f"Name {result.inventory_id}")
# inventory = results.scalars().all()
# for item in inventory:
#     print(f"Customer: {item.film_id}, Staff: {item.inventory_id}, Inventory: {item.last_update}, Last Update: {item.store_id}")

# I need a list of films that have been rented out and those not

# Available Films
def available_films():
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
        session.query(
            inventory.inventory_id,
            film.film_id,
            film.title,

        )
        .join(inventory, film.film_id == inventory.film_id)
        .join(rental, inventory.inventory_id == rental.inventory_id)
        .filter(rental.return_date.isnot(None))
    )

    never_rented = (
        session.query(
            inventory.inventory_id,
            film.film_id,
            film.title,

        )
        .outerjoin(inventory, film.film_id == inventory.film_id)
        .outerjoin(rental, inventory.inventory_id == rental.inventory_id)
        .filter(rental.rental_id.is_(None))
    )

    combined_query = rented_and_returned.union_all(never_rented)
    results = session.execute(combined_query).fetchall()

    for result in results:
        print(result[0], result[1], result[2])

# Select film title, film id, inventory id, customer name, rental id and rental date which is for available rented out films



available_films()