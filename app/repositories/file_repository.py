from models import db
from flask import current_app

class FileRepository:
    def __init__(self, db):
        self.db = db

    def save_all_files(self, image, screenshots, game_file):
        pass
