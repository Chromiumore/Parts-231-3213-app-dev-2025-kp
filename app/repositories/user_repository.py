from app.models import Game, User
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256

class UserRepository:
    def __init__(self, db):
        self.db : SQLAlchemy = db

    def all(self):
        query = self.db.select(User)
        return self.db.session.execute(query).all()
    
    def get_user_by_id(self, id):
        query = self.db.select(User).filter_by(id=id)
        return self.db.session.execute(query).scalar()
    
    def get_user_by_username_and_password(self, username, password):
        query = self.db.select(User).where(username == User.username, sha256(password.encode()).hexdigest() == User.password_hash)
        return self.db.session.execute(query).scalar()
