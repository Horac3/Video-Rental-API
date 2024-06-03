# To connect, you need SQLAlchemy engine
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model.inventory import InventoryModel
from model.rental import RentalModel

engine = create_engine("mysql://root:121096@localhost/sakila")
try:
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print("Error occurred:", e)

session = Session(engine)

stmt = select(RentalModel)
result = session.execute(stmt)
rental = result.scalars().all()
for item in rental:
    print(f"Customer: {item.customer.first_name}, Staff: {item.staff.first_name}, Inventory: {item.inventory.film_id}, Last Update: {item.last_update}")
