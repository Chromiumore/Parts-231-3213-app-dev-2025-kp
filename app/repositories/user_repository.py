from app.models import Game, User, Role
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from hashlib import sha256

class UserRepository:
    def __init__(self, db):
        self.db : SQLAlchemy = db

    def create(self, username, password, role_id):
        user = User(
            username=username,
            password_hash=sha256(password.encode()).hexdigest(),
            role_id=role_id
        )
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return self.get_user_by_username_and_password(username, password)
    
    def delete(self, id):
        try:
            self.db.session.query(User).where(User.id == id).delete()
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True

    def all(self):
        query = self.db.select(User)
        return self.db.session.execute(query).all()
    
    def get_user_by_id(self, id):
        query = self.db.select(User).filter_by(id=id)
        return self.db.session.execute(query).scalar()
    
    def get_user_by_username_and_password(self, username, password):
        query = self.db.select(User).where(username == User.username, sha256(password.encode()).hexdigest() == User.password_hash)
        return self.db.session.execute(query).scalar()
    
    def get_author(self, game_id):
        query = self.db.select(User).join(Game, User.id == Game.user_id).where(Game.id == game_id)
        return self.db.session.execute(query).scalar()
    
    def get_number_of_users(self):
        query = self.db.select(func.count()).select_from(User)
        return self.db.session.execute(query).scalar()
    
    def get_number_of_developers(self):
        query = self.db.select(func.count(User.id.distinct())).select_from(User).join(Game, Game.user_id == User.id)
        return self.db.session.execute(query).scalar()
    
    def get_user_role(self, user_id):
        query = self.db.select(Role).join(User, User.role_id == Role.id).where(User.id == user_id)
        return self.db.session.execute(query).scalar()
