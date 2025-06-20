from flask_sqlalchemy import SQLAlchemy

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
