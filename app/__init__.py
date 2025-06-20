from flask import Flask
from flask_migrate import Migrate
from . import games, auth, uploads, creator_hub, moderation
from .models import db
from .repositories.game_repository import GameRepository

game_repository = GameRepository(db)

migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    db.init_app(app)
    migrate.init_app(app, db)

    auth.init_login_manager(app)
    app.register_blueprint(auth.bp)

    app.register_blueprint(games.bp)
    app.route('/')(games.default)

    app.register_blueprint(uploads.bp)
    app.register_blueprint(creator_hub.bp)
    app.register_blueprint(moderation.bp)

    return app
