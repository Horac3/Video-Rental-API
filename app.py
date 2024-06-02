# To connect, you need SQLAlchemy engine
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model.inventory import InventoryModel

engine = create_engine("mysql://root:121096@localhost/sakila")
try:
    with engine.connect() as connection:
        print("Connection successful")
except Exception as e:
    print("Error occurred:", e)

session = Session(engine)

stmt = select(InventoryModel)
result = session.execute(stmt)
inventory = result.scalars().all()
for item in inventory:
    print(f"Inventory ID: {item.inventory_id}, Film ID: {item.film_id}, Store ID: {item.store_id}, Last Update: {item.last_update}")
