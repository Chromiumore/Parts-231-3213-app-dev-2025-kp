from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .repositories.game_repository import GameRepository
from .repositories.user_repository import UserRepository
from .models import db

bp = Blueprint('games', __name__)

game_repository = GameRepository(db)
user_repository = UserRepository(db)

@bp.route('/')
def index():
    games = game_repository.all()
    return render_template('index.html', games = games)

@bp.route('/creatorhub')
@login_required
def creator_hub():
    games = game_repository.get_games_by_user_id(current_user.id)
    user = user_repository.get_user_by_id(current_user.id)
    return render_template('creator_hub.html', games=games, user=user)
