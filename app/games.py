import json
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, make_response, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .repositories.game_repository import GameRepository, Game
from .repositories.user_repository import UserRepository
from .repositories.os_repository import OSRepository
from .models import db

bp = Blueprint('games', __name__)

game_repository = GameRepository(db)
user_repository = UserRepository(db)
os_repository = OSRepository(db)

def user_has_rights(func):
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


@bp.route('/')
def index():
    games = game_repository.all()
    return render_template('index.html', games = games)

@bp.route('/creatorhub')
@login_required
def creator_hub():
    games = game_repository.get_games_by_user_id(current_user.id)
    user = user_repository.get_user_by_id(current_user.id)
    return render_template('creator-hub.html', games=games, user=user)

@bp.route('/creatorhub/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        form = request.form
        os_ids = form.getlist('os-list')
        new_game = Game(
            name = form.get('name'),
            user_id = current_user.id,
            description = form.get('description'),
            info = form.get('info')
        )

        os_list = list(map(os_repository.get_by_id, os_ids))

        is_successful = game_repository.create(new_game, os_list)

        if is_successful:
            flash('Игра успешно загружена', 'success')
            return redirect(url_for('games.creator_hub'))
        else:
            flash('Не удалось загрузить игру. Попробуйте позже', 'success')
    
    os = os_repository.get_all_and_game_has_by_id()
    return render_template('upload.html', os=os)

@bp.route('/creatorhub/update/<game_id>', methods=['POST', 'GET'])
@login_required
@user_has_rights
def update(game_id):
    game = game_repository.get_game_by_id(game_id)
    if not game:
        return abort(404)
    if request.method == 'POST':
        if game:
            updated_game = Game(
                id=game_id,
                name=request.form.get('name'),
                user_id=current_user.id,
                description=request.form.get('description'),
                info=request.form.get('info'),
                last_updated_at=datetime.now()
            )

            is_successful = game_repository.update(game_id, updated_game)
            if is_successful:
                flash('Игра успешно загружена', 'success')
                return redirect(url_for('games.creator_hub'))
            else:
                flash('Не удалось загрузить игру. Попробуйте позже', 'success')

    os_info = os_repository.get_all_and_game_has_by_id(game_id)
    print(os_info)
    return render_template('update.html', game=game, os=os_info) 

@bp.route('/creatorhub/delete/<game_id>', methods=['GET'])
@login_required
@user_has_rights
def delete(game_id):
    is_successful = game_repository.delete(game_id)

    if is_successful:
        flash('Игра успешно удалена', 'success')
    else:
        flash('Не удалось удалить игру', 'error')
            
    return redirect(url_for('games.creator_hub'))
