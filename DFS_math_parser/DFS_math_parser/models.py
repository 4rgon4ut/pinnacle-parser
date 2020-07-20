import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Set DB connection details

USER = ''
PASSWORD = ''
DATABASE = ''

engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@localhost:5432/{DATABASE}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

