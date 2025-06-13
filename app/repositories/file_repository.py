from app.models import db, File, FileType
from flask import current_app

class FileRepository:
    def __init__(self, db):
        self.db = db
    
    def get_file_by_id(self, id):
        query = self.db.select(File).filter_by(id=id)
        return self.db.session.execute(query).scalar()
    
    def get_file_by_storage_name(self, name):
        query = self.db.select(File).filter_by(storage_name=name)
        return self.db.session.execute(query).scalar()
    
    def get_files_by_game_id(self, game_id):
        query = self.db.select(File).where(File.game_id == game_id)
        return self.db.session.execute(query).scalars()
    
    def create(self, file):
        try:
            self.db.session.add(file)
            self.db.session.commit()
        except Exception as e:
            self.db.session.rollback()
            raise e
        return True
    
