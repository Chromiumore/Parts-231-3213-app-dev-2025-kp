from app.models import db, File
from flask import current_app
from sqlalchemy import and_

class FileRepository:
    def __init__(self, db):
        self.db = db
    
    def get_file_by_id(self, id):
        query = self.db.select(File).filter_by(id=id)
        return self.db.session.execute(query).scalar()
    
    def get_file_by_storage_name(self, name):
        query = self.db.select(File).filter_by(storage_name=name)
        return self.db.session.execute(query).scalar()
    
    def get_media_by_game_id(self, game_id):
        query = self.db.select(File).where(and_(File.game_id == game_id, File.file_type in ('main_image', 'screenshot'))).order_by(
                                                                            db.case((File.file_type == 'main_image', 1), else_=2))
        return self.db.session.execute(query).scalars()
    
    def get_source_by_game_id(self, game_id):
        query = self.db.select(File).where(and_(File.game_id == game_id, File.file_type == 'source'))
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
    
