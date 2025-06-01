from app.models import User, Role
from flask_sqlalchemy import SQLAlchemy

class RoleRepository:
    def __init__(self, db):
        self.db = db

    def get_role_by_name(self, name):
        query = self.db.select(Role).where(Role.name == name)
        return self.db.session.execute(query).scalar()
