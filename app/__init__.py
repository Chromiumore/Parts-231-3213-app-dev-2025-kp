from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import games, auth
from .models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    db.init_app(app)
    migrate.init_app(app, db)

    auth.init_login_manager(app)
    app.register_blueprint(auth.bp)

    app.register_blueprint(games.bp)

    return app