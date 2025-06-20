from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from .repositories.game_repository import GameRepository
from .repositories.stats_repository import StatsRepository
from .repositories.role_repository import RoleRepository
from .repositories.user_repository import UserRepository
from .models import db

game_repository = GameRepository(db)
stats_repository = StatsRepository(db)
role_repository = RoleRepository(db)
user_repository = UserRepository(db)

def permission_required(only_moderator=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                user_id = current_user.id
                game = game_repository.get_game_by_id(kwargs.get('game_id'))
                role = user_repository.get_user_role(user_id)
                if role.name == 'moderator' or ((game is None or game.user_id == user_id) and not only_moderator):
                    return func(*args, **kwargs)
                
                flash('У вас недостаточно прав для данного действия', 'warning')
                return redirect(url_for('games.index'))
        return wrapper
    return decorator

def track_game_visits(func):
    @wraps(func)
    def wrapper(game_id):
        stats_repository.inc_visits(game_id)
        return func(game_id)
    return wrapper

def track_game_downloads(func):
    @wraps(func)
    def wrapper(filename):
        game = game_repository.get_game_by_source(filename)
        if game:
            stats_repository.inc_downloads(game.id)
        return func(filename)
    return wrapper
