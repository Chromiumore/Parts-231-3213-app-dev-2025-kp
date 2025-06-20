from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func, label
from app.models import OS, Game

class OSRepository:
    def __init__(self, db : SQLAlchemy):
        self.db = db
    
    def all(self):
        query = self.db.select(OS)
        return self.db.session.execute(query).scalars()
    
    def get_by_id(self, id):
        query = self.db.select(OS).filter_by(id=id)
        return self.db.session.execute(query).scalar()

    def get_by_name(self, name):
        query = self.db.select(OS).filter_by(name=name)
        return self.db.session.execute(query).scalar()

    def get_game_supported_os(self, game_id):
        query = self.db.select(OS).join(OS.games).where(Game.id == game_id)
        return self.db.session.execute(query).scalars()

    def get_all_and_game_has_by_id(self, game_id=None):
        if game_id is not None:
            query = self.db.select(OS, Game.id.is_not(None).label('has')).outerjoin(OS.games).where(or_(Game.id == game_id, Game.id.is_(None)))
        else:
            query = self.db.select(OS, None)
        return self.db.session.execute(query).all()
