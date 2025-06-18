from flask_sqlalchemy import SQLAlchemy
from app.models import VisitLog, Game
from sqlalchemy import func

class VisitRepository:
    def __init__(self, db : SQLAlchemy):
        self.db = db

    def create(self, log):
        try:
            self.db.session.add(log)
            self.db.session.commit()
            self.db.session.refresh(log)
        except Exception as e:
            self.db.session.rollback()
            raise e
        return log
    
    def get_number_of_path_visits(self, path):
        query = self.db.select(func.count()).select_from(VisitLog).where(path == VisitLog.path)
        return self.db.session.execute(query).scalar()
