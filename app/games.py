from flask import Blueprint, render_template, url_for, abort, current_app
from markdown import markdown
from .repositories.game_repository import GameRepository
from .repositories.user_repository import UserRepository
from .repositories.os_repository import OSRepository
from .repositories.file_repository import FileRepository
from .repositories.visit_repository import VisitRepository
from .models import db

bp = Blueprint('games', __name__)

game_repository = GameRepository(db)
user_repository = UserRepository(db)
os_repository = OSRepository(db)
file_repository = FileRepository(db)
visit_repository = VisitRepository(db)
        

@bp.route('/')
def index():
    games = game_repository.all()
    games_info = []
    for game in games:
        games_info.append([game, user_repository.get_author(game.id), os_repository.get_game_supported_os(game.id),
                           file_repository.get_main_image_by_game_id(game.id)])
    return render_template('index.html', games_info = games_info)

@bp.route('/<int:game_id>')
def view_game(game_id):
    game_info = game_repository.get_game_and_user_by_id(game_id)
    if not game_info:
        abort(404)
    
    game, author = list(game_info)
    supported_os = os_repository.get_game_supported_os(game_id)
    media = file_repository.get_media_by_game_id(game_id)
    source = file_repository.get_source_by_game_id(game_id)
    game_downloads = visit_repository.get_number_of_path_visits(url_for('uploads.send_uploaded_file', filename=source.storage_name))
    game_views = visit_repository.get_number_of_path_visits(url_for('games.view_game', game_id=game_id))
    return render_template('view-game.html', game=game, author=author, path=current_app.config['UPLOAD_FOLDER'],
                            supported_os=supported_os, media=list(media), source=source, info_markdown=markdown(game.info),
                            downloads=game_downloads, views=game_views)
