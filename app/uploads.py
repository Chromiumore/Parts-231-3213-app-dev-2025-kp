from flask import Blueprint, current_app, send_from_directory, abort
from .repositories.file_repository import FileRepository
from .models import db

bp = Blueprint('uploads', __name__, url_prefix='/uploads')

file_repository = FileRepository(db)

@bp.route('/<filename>')
def send_uploaded_file(filename=''):
    file = file_repository.get_file_by_storage_name(filename)
    if not file:
        abort(404)
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename, download_name=file.original_name)