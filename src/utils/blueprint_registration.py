from src.inventory.routes.inventory_routes import blp as InventoryRoute

def register_blueprints(api):
    api.register_blueprint(InventoryRoute)

