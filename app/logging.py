from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from .repositories.game_repository import GameRepository
from .models import db

game_repository = GameRepository(db)

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