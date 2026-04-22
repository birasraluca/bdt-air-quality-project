from flask import Flask
from app.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    app.register_blueprint(api_bp)

    return app