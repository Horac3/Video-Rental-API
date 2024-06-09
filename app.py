from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api

from src.utils.db import db
from src.utils.app_configuration import configure_app
from src.utils.blueprint_registration import register_blueprints
from src.utils.jwt_setup import setup_jwt



def create_app(db_url=None):
    app = Flask(__name__)
    configure_app(app)
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    setup_jwt(app)

    with app.app_context():
        db.create_all()

    register_blueprints(api)

    return app

if __name__ == '__main__':
    app = create_app("mysql://username:password@localhost/dbname")
    app.run(debug=True)
