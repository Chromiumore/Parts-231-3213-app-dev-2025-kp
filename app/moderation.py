from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required
from .models import db
from .repositories.game_repository import GameRepository
from .repositories.user_repository import UserRepository
from .repositories.stats_repository import StatsRepository
from .tools import permission_required

bp = Blueprint('moderation', __name__, url_prefix='/moderation')

game_repository = GameRepository(db)
stats_repository = StatsRepository(db)
user_repository = UserRepository(db)

@bp.route('/stats')
@login_required
@permission_required(only_moderator=True)
def stats():
    total_games = game_repository.get_number_of_games()
    total_downloads = stats_repository.get_total_downloads()
    total_users = user_repository.get_number_of_users()
    total_developers = user_repository.get_number_of_developers()

    top_downloaded = stats_repository.get_most_downloaded_games(10)
    downloaded_names = [el[0].name for el in top_downloaded]
    downloaded_numbers = [el[1].downloads for el in top_downloaded]

    top_visited = stats_repository.get_most_visited_games(10)
    visited_names = [el[0].name for el in top_visited]
    visited_numbers = [el[1].visits for el in top_visited]

    os_stats = stats_repository.get_os_stats()
    os_names = [el[0].display_name for el in os_stats]
    os_numbers = [el[1] for el in os_stats]
    os_percents = [0 if sum(os_numbers) == 0 else round((el*100)/sum(os_numbers)) for el in os_numbers]

    return render_template('global-stats.html', total_games=total_games, total_downloads=total_downloads,
                           total_users=total_users, total_developers=total_developers, downloaded_names=downloaded_names,
                           downloaded_numbers=downloaded_numbers, visited_names=visited_names, visited_numbers=visited_numbers,
                           os_names=os_names, os_percents=os_percents)

@bp.route('/ban/<user_id>', methods=['POST'])
@login_required
@permission_required(only_moderator=True)
def ban(user_id):
    user_repository.delete(user_id)
    flash('Пользователь успешно заблокирован', 'success')
    return redirect(url_for('games.index'))
