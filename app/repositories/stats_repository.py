from sqlalchemy import func
from app.models import GameStats, Game, OS

class StatsRepository:
    def __init__(self, db):
        self.db = db

    def create(self, game_id):
        stats = GameStats(game_id=game_id)
        try:
            self.db.session.add(stats)
            self.db.session.commit()
            self.db.session.refresh(stats)
        except Exception as e:
            self.db.session.rollback()
            raise e
        return stats

    def get_downloads(self, game_id):
        query = self.db.select(GameStats.downloads).where(GameStats.game_id == game_id)
        return self.db.session.execute(query).scalar()
    
    def get_visits(self, game_id):
        query = self.db.select(GameStats.visits).where(GameStats.game_id == game_id)
        return self.db.session.execute(query).scalar()
    
    def get_most_downloaded_games(self, limit=None):
        query = self.db.select(Game, GameStats).join(GameStats, Game.id == GameStats.game_id).order_by(GameStats.downloads.desc()).limit(limit)
        return self.db.session.execute(query).all()
    
    def get_most_visited_games(self, limit=None):
        query = self.db.select(Game, GameStats).join(GameStats, Game.id == GameStats.game_id).order_by(GameStats.visits.desc()).limit(limit)
        return self.db.session.execute(query).all()
    
    def get_total_downloads(self):
        query = self.db.select(func.sum(GameStats.downloads)).select_from(GameStats)
        return self.db.session.execute(query).scalar()
    
    def get_total_visits(self):
        query = self.db.select(func.sum(GameStats.visits)).select_from(GameStats)
        return self.db.session.execute(query).scalar()
    
    def inc_visits(self, game_id):
        try:
            self.db.session.query(GameStats).where(GameStats.game_id == game_id).update({'visits' : GameStats.visits + 1})
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        
    def inc_downloads(self, game_id):
        try:
            self.db.session.query(GameStats).where(GameStats.game_id == game_id).update({'downloads' : GameStats.downloads + 1})
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
    
    def get_os_stats(self):
        query = self.db.select(OS, func.count(Game.id)).select_from(OS).outerjoin(OS.games).group_by(OS.id).order_by(OS.id)
        return self.db.session.execute(query).all()
