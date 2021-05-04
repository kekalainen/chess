from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Game(Base):
    """An ORM model representing a game."""
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pgn = Column(String)
