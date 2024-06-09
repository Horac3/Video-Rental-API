import os

def configure_app(app):
    app.config["API_TITLE"] =                os.getenv("API_TITLE")
    app.config["API_VERSION"] = os.getenv("API_VERSION")
    app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION")
    app.config["OPENAPI_URL_PREFIX"] = os.getenv("OPENAPI_URL_PREFIX")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.getenv("OPENAPI_SWAGGER_UI_PATH")
    app.config["OPENAPI_SWAGGER_UI_URL"] = os.getenv("OPENAPI_SWAGGER_UI_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == 'true'
    app.config["PROPAGATE_EXCEPTIONS"] = os.getenv("PROPAGATE_EXCEPTIONS", "True").lower() == 'true'
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
