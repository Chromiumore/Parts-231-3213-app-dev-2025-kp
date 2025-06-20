from flask import Blueprint, request
from flask_login import current_user
from .repositories.visit_repository import VisitRepository
from .models import db, VisitLog

visit_repository = VisitRepository(db)

bp = Blueprint('logging', __name__)

@bp.before_app_request
def save_visit_log():
    log = VisitLog(
        path = request.path,
        user_id = current_user.id if current_user.is_authenticated else None
    )
    visit_repository.create(log)
