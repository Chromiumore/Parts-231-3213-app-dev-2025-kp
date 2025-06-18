from functools import wraps
from flask import Flask, request, flash, redirect, url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import games, auth, uploads, creator_hub
from .models import db, VisitLog
from .repositories.visit_repository import VisitRepository
from .repositories.game_repository import GameRepository

visit_repository = VisitRepository(db)
game_repository = GameRepository(db)

migrate = Migrate()

@games.bp.after_request
@uploads.bp.after_request
def save_visit_log(response):
    if request.method == 'GET' and response.status_code not in (404, 500):
        log = VisitLog(
            path = request.path,
            user_id = current_user.id if current_user.is_authenticated else None
        )
        visit_repository.create(log)
    return response


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    db.init_app(app)
    migrate.init_app(app, db)

    auth.init_login_manager(app)
    app.register_blueprint(auth.bp)

    app.register_blueprint(games.bp)
    app.register_blueprint(uploads.bp)
    app.register_blueprint(creator_hub.bp)

    return app
