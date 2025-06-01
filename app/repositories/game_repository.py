from app.models import Game, User
from flask_sqlalchemy import SQLAlchemy

class GameRepository:
    def __init__(self, db):
        self.db : SQLAlchemy = db

    def all(self):
        query = self.db.select(Game).join(User, Game.user_id == User.id)
        return self.db.session.execute(query).scalars()
    
    def get_game_by_id(self, id):
        query = self.db.select(Game).filter_by(id=id)
        return self.db.session.execute(query).scalar()
    
    def get_games_by_user_id(self, user_id):
        query = self.db.select(Game).where(Game.user_id == user_id)
        return self.db.session.execute(query).scalars()
    
    def create(self, game):
        try:
            self.db.session.add(game)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True
    
    def update(self, id, game):
        try:
            self.db.session.query(Game).where(Game.id == id).update({
                Game.name: game.name,
                Game.user_id: game.user_id,
                Game.description: game.description,
                Game.info: game.info,
                Game.last_updated_at: game.last_updated_at
            })
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True

    def delete(self, id):
        try:
            self.db.session.query(Game).where(Game.id == id).delete()
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True

