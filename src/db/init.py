from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

db_engine = create_engine("sqlite:///db.sqlite")
db_session = sessionmaker(bind=db_engine)()

Base.metadata.create_all(db_engine)
