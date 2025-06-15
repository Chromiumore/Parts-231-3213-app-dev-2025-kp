from app.models import Game, User
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
from sqlalchemy import and_

class UserRepository:
    def __init__(self, db):
        self.db : SQLAlchemy = db

    def create(self, username, password, role_name='default'):
        user = User(
            username=username,
            password_hash=sha256(password.encode()).hexdigest(),
            role_name=role_name
        )
        try:
            self.db.session.add(user)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return self.get_user_by_username_and_password(username, password)

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
        query = self.db.select(User).where(and_(User.id == Game.user_id, Game.id == game_id))
        self.db.session.execute(query).scalar()
