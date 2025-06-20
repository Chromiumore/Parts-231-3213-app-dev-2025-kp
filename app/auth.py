from flask import request, Blueprint, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from .repositories.user_repository import UserRepository
from .repositories.role_repository import RoleRepository
from .models import db

user_repository = UserRepository(db)
role_repository = RoleRepository(db)

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
        remember_me = request.form.get('remember_me')
        if username and password:
            user = user_repository.get_user_by_username_and_password(username, password)
            if user:
                login_user(user, remember=remember_me)
                flash('Вы успешно аутентифицированы.', 'success')
                return redirect(url_for('games.index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('login.html')

@bp.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_conf = request.form.get('password-confirm')
        remember_me = request.form.get('remember_me')
        if username and password and (password == password_conf):
            default_role = role_repository.get_role_by_name('default')
            user = user_repository.create(username, password, default_role.id)
            if user:
                login_user(user, remember=remember_me)
                flash('Вы успешно зарегистрировались.', 'success')
                return redirect(url_for('games.index'))
        flash('Не удалось зарегистрироваться. Проверьте правильность заполнения полей', 'danger')
    return render_template('registration.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('games.index'))