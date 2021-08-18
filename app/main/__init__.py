from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from app.main.util import logs
import logging

from .config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
logs.initialize_logger("movies_api")

def create_app(config_name: str):
    """create a flask application"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app,db)
    flask_bcrypt.init_app(app)

    return app