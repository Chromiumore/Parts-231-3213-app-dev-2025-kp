from flask import request, Blueprint, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from .repositories.user_repository import UserRepository
from .models import db

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    return user_repository.get_user_by_id(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = user_repository.get_user_by_username_and_password(username, password)
            if user:
                login_user(user)
                flash('Вы успешно аутентифицированы.', 'success')
                return redirect(url_for('games.index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('games.index'))