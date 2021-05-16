from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Game(Base):
    """An ORM model representing a game."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pgn = Column(String)

class Setting(Base):
    """An ORM model for settings."""
    __tablename__ = "settings"

    name = Column(String, primary_key=True)
    value = Column(String)
