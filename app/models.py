from datetime import datetime
from typing import Optional, List
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import MetaData, String, ForeignKey, Text, Table, Column, Enum, Integer
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(model_class=Base)

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password_hash: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))

class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    display_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text())

GameOs = Table(
    'games_os',
    Base.metadata,
    Column('game_id', ForeignKey('games.id', ondelete='CASCADE'), primary_key=True),
    Column('os_id', ForeignKey('os.id'), primary_key=True)
)

class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    description: Mapped[Optional[str]] = mapped_column(String(150))
    info: Mapped[Optional[str]] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    os_list: Mapped[List['OS']] = relationship('OS', secondary=GameOs, back_populates='games')

class OS(Base):
    __tablename__ = 'os'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    display_name: Mapped[str] = mapped_column(String(50))
    fa_icon_name: Mapped[str] = mapped_column(String(50))
    games: Mapped[List['Game']] = relationship('Game', secondary=GameOs, back_populates='os_list')

class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_name: Mapped[str] = mapped_column(String(256), unique=True)
    original_name: Mapped[str] = mapped_column(String(256))
    file_type: Mapped[str] = mapped_column(Enum('main_image', 'screenshot', 'source'))
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id, ondelete='CASCADE'))

class VisitLog(Base):
    __tablename__ = 'visit_logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

class GameStats(Base):
    __tablename__ = 'games_stats'

    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id, ondelete='CASCADE'), primary_key=True)
    visits: Mapped[int] = mapped_column(Integer, default=0)
    downloads: Mapped[int] = mapped_column(Integer, default=0)
