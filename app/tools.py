from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from .repositories.game_repository import GameRepository
from .repositories.stats_repository import StatsRepository
from .models import db

game_repository = GameRepository(db)
stats_repository = StatsRepository(db)


def permission_required(func):
    @wraps(func)
    def inner(game_id):
        user_id = current_user.id
        game = game_repository.get_game_by_id(game_id)
        if game is None or game.user_id == user_id:
            return func(game_id)
        else:
            flash('У вас недостаточно прав для данного действия', 'warning')
            return redirect(url_for('games.index'))
    return inner

def track_game_visits(func):
    @wraps(func)
    def inner(game_id):
        stats_repository.inc_visits(game_id)
        return func(game_id)
    return inner

def track_game_downloads(func):
    @wraps(func)
    def inner(filename):
        game = game_repository.get_game_by_source(filename)
        if game:
            stats_repository.inc_downloads(game.id)
        return func(filename)
    return inner
