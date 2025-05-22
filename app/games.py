from flask import Blueprint, render_template
from .repositories.game_repository import GameRepository
from .models import db

bp = Blueprint('games', __name__)

game_repository = GameRepository(db)

@bp.route('/')
def index():
    games = game_repository.all()
    return render_template('index.html', games = games)
