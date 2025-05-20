from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import games

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    app.register_blueprint(games.bp)

    return app