import os
from datetime import datetime
from uuid import uuid4
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from .repositories.game_repository import GameRepository, Game
from .repositories.user_repository import UserRepository
from .repositories.os_repository import OSRepository
from .repositories.file_repository import FileRepository, File
from .repositories.stats_repository import StatsRepository
from .models import db
from .tools import permission_required

bp = Blueprint('creator_hub', __name__, url_prefix='/creator-hub')

game_repository = GameRepository(db)
file_repository = FileRepository(db)
stats_repositroy = StatsRepository(db)
os_repository = OSRepository(db)
user_repository = UserRepository(db)

def gen_storage_filename(filename):
    prefix = str(uuid4())
    return f"{prefix}-{filename}"


@bp.route('/')
@login_required
def creator_hub():
    games_info = []
    games = game_repository.get_games_by_user_id(current_user.id)
    for game in games:
        game_downloads = stats_repositroy.get_downloads(game.id)
        game_visits = stats_repositroy.get_visits(game.id)
        games_info.append([game, file_repository.get_main_image_by_game_id(game.id),
                           os_repository.get_game_supported_os(game.id), game_downloads, game_visits])
    user = user_repository.get_user_by_id(current_user.id)
    return render_template('creator-hub.html', games_info=games_info, user=user)

@bp.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        form = request.form

        main_image = request.files.get('main-image')
        screenshots = request.files.getlist('screenshots')
        source_file = request.files.get('game-files')
        
        os_ids = form.getlist('os-list')
        new_game = Game(
            name = form.get('name'),
            user_id = current_user.id,
            description = form.get('description'),
            info = form.get('info')
        )

        os_list = list(map(os_repository.get_by_id, os_ids))

        created_game = game_repository.create(new_game, os_list)
        stats_repositroy.create(created_game.id)
        
        m_img_storage_name = gen_storage_filename(main_image.filename)
        file_repository.create(File(
                storage_name = m_img_storage_name,
                original_name = main_image.filename,
                file_type = 'main_image',
                game_id = new_game.id
            ))
        main_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], m_img_storage_name))
        
        for s in screenshots:
            s_storage_name = gen_storage_filename(s.filename)
            file_repository.create(File(
                storage_name = s_storage_name,
                original_name = s.filename,
                file_type = 'screenshot',
                game_id = new_game.id
            ))
            s.save(os.path.join(current_app.config['UPLOAD_FOLDER'], s_storage_name))

        src_storage_name = gen_storage_filename(source_file.filename)
        file_repository.create(File(
                storage_name = src_storage_name,
                original_name = source_file.filename,
                file_type = 'source',
                game_id = new_game.id
            ))
        source_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], src_storage_name))

        if created_game:
            flash('Игра успешно загружена', 'success')
            return redirect(url_for('creator_hub.creator_hub'))
        else:
            flash('Не удалось загрузить игру. Попробуйте позже', 'success')
    
    game_os = os_repository.get_all_and_game_has_by_id()
    return render_template('upload.html', os=game_os)

@bp.route('/update/<game_id>', methods=['POST', 'GET'])
@login_required
@permission_required()
def update(game_id):
    game = game_repository.get_game_by_id(game_id) 
    if request.method == 'POST':
        main_image = request.files.get('main-image')
        screenshots = request.files.getlist('screenshots')
        source_file = request.files.get('game-files')
        if game:
            updated_game = Game(
                id=game_id,
                name=request.form.get('name'),
                user_id=current_user.id,
                description=request.form.get('description'),
                info=request.form.get('info'),
                last_updated_at=datetime.now()
            )

            created_game = game_repository.update(game_id, updated_game)
            
            old_game_files = file_repository.get_files_by_game_id(game_id)

            file_repository.remove_files()
            for file in old_game_files:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file.storage_name))

            m_img_storage_name = gen_storage_filename(main_image.filename)
            file_repository.create(File(
                    storage_name = m_img_storage_name,
                    original_name = main_image.filename,
                    file_type = 'main_image',
                    game_id = updated_game.id
                ))
            main_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], m_img_storage_name))
        
            for s in screenshots:
                s_storage_name = gen_storage_filename(s.filename)
                file_repository.create(File(
                    storage_name = s_storage_name,
                    original_name = s.filename,
                    file_type = 'screenshot',
                    game_id = updated_game.id
                ))
                s.save(os.path.join(current_app.config['UPLOAD_FOLDER'], s_storage_name))

            src_storage_name = gen_storage_filename(source_file.filename)
            file_repository.create(File(
                    storage_name = src_storage_name,
                    original_name = source_file.filename,
                    file_type = 'source',
                    game_id = updated_game.id
                ))
            source_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], src_storage_name))

            if created_game:
                flash('Игра успешно загружена', 'success')
                return redirect(url_for('creator_hub.creator_hub'))
            else:
                flash('Не удалось загрузить игру. Попробуйте позже', 'success')

    if game:
        os_info = os_repository.get_all_and_game_has_by_id(game_id)
        return render_template('update.html', game=game, os=os_info)
    abort(404)

@bp.route('/delete/<game_id>', methods=['GET'])
@login_required
@permission_required()
def delete(game_id):
    game_files = file_repository.get_files_by_game_id(game_id)

    is_successful = game_repository.delete(game_id)

    for file in game_files:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file.storage_name))
    
    if is_successful:
        flash('Игра успешно удалена', 'success')
    else:
        flash('Не удалось удалить игру', 'error')
            
    return redirect(url_for('creator_hub.creator_hub'))