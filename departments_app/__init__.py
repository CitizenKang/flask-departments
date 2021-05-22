from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    """
    Creates Flask instance, configures, registers extensions, add routes
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ma.init_app(app)

    from .rest import rest_api_bp as rest_blueprint
    app.register_blueprint(rest_blueprint)

    return app
