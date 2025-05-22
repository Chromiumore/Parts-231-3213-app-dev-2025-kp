from app.models import Game, User
from flask_sqlalchemy import SQLAlchemy

class GameRepository:
    def __init__(self, db):
        self.db : SQLAlchemy = db

    def all(self):
        query = self.db.select(Game).join(User, Game.user_id == User.id)
        return self.db.session.execute(query).all()
    
    def get_game_by_id(self, id):
        query = self.db.select(Game).join(User, Game.user_id == User.id).where(Game.id == id)
        return self.db.session.execute(query).first()
    
    def create(self, id, name, user_id, description, info, created_at, last_updated_at):
        game = Game(
            id=id,
            name=name,
            user_id=user_id,
            description=description,
            info=info
        )
        try:
            self.db.session.add(game)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return game
