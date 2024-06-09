# To connect, you need SQLAlchemy engine
from sqlalchemy import create_engine, literal, select
from sqlalchemy.orm import Session, sessionmaker, aliased
from src.film.model.film_model import FilmModel
from src.inventory.model.inventory_model import InventoryModel
from src.rental.model.rental_model import RentalModel
from sqlalchemy.sql import func
from datetime import datetime

engine = create_engine("mysql://root:121096@localhost/sakila")
try:
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print("Error occurred:", e)

session = Session(engine)

film = aliased(FilmModel)
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
            FilmModel.film_id,
            FilmModel.title,
            literal('Rented and Returned').label('status')
        )
        .join(inventory, FilmModel.film_id == inventory.film_id)
        .join(rental, inventory.inventory_id == rental.inventory_id)
        .filter(rental.return_date.isnot(None))
    )

    # Query for films that have never been rented out
    never_rented = (
        session.query(
            inventory.inventory_id,
            FilmModel.film_id,
            FilmModel.title,
            literal('Never Rented').label('status')
        )
        .outerjoin(inventory, FilmModel.film_id == inventory.film_id)
        .outerjoin(rental, inventory.inventory_id == rental.inventory_id)
        .filter(rental.rental_id.is_(None))
    )

    # Combine the two queries using union_all
    combined_query = rented_and_returned.union_all(never_rented)
    results = session.execute(combined_query).fetchall()

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
# Select film title, film id, inventory id, customer name, rental id and rental date which is for available rented out films

# Function to allow renting
def rent(intventory_id, customer_id, staff_id):
    try:
        # Check if the record exists
        existing_rental = session.query(RentalModel).filter_by(
            inventory_id=intventory_id,
            return_date=None
        ).first()

        if existing_rental:
            print("The rental record already exists.")
            session.rollback()
        else:
            # Insert the new record
            rental = RentalModel(
                rental_date=datetime.now(),
                inventory_id=intventory_id,
                customer_id=customer_id,
                return_date=None,
                staff_id=staff_id,
                last_update=datetime.now()
            )
            session.add(rental)
            session.commit()
            print("The rental record has been added.")
    except Exception as e:
        print(f"An exception occurred: {e}")
        session.rollback()  # Rollback the session in case of an exception
    finally:
        session.close()


def returnFilm(inventory_id):
    try:
        # Query the rental record to update, including the film title
        rental_record = session.query(RentalModel, FilmModel.title).join(
            InventoryModel, RentalModel.inventory_id == InventoryModel.inventory_id
        ).join(
            FilmModel, InventoryModel.film_id == FilmModel.film_id
        ).filter(
            RentalModel.inventory_id == inventory_id,
            RentalModel.return_date.is_(None)
        ).first()

        if rental_record:
            # Update the return date
            rental = rental_record[0]
            rental.return_date = datetime.now()
            session.commit()
            film_title = rental_record[1]
            print(f"Film '{film_title}' with inventory_id {inventory_id} has been returned.")
            return film_title
        else:
            print(f"No active rental found for inventory_id {inventory_id}.")
            return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        session.rollback()
        return None
    finally:
        session.close()


returned_film_title = returnFilm(1)
if returned_film_title:
    print(f"Returned film title: {returned_film_title}")