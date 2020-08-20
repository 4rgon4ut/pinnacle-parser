from .settings import DATABASE_SETTINGS

from sqlalchemy import Column, JSON, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

USER = DATABASE_SETTINGS['user']
PASSWORD = DATABASE_SETTINGS['password']
DATABASE = DATABASE_SETTINGS['database']

engine = create_engine(
    f'postgresql+psycopg2://{USER}:{PASSWORD}@localhost:5432/{DATABASE}'
)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Group(Base):
    """Groups of commands by parts of the world"""
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    # Some methods??

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Group: {self.name}'


class League(Base):
    """Sport leagues"""
    __tablename__ = 'Leagues'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<League: {self.name}>'


class Map(Base):
    """Single map data object"""
    __tablename__ = 'Maps'

    id = Column(Integer, primary_key=True, nullable=False)

    group = relationship('Group', backref='maps')
    group_id = Column(Integer, ForeignKey('Groups.id'))

    league = relationship('League', backref='maps')
    league_ld = Column(Integer, ForeignKey('Leagues.id'))

    map_number = Column(Integer)  # ?nullable=False?
    team1 = Column(String(99))
    team2 = Column(String(99))
    data = Column(JSON)
    team_line = relationship('TeamLine', uselist=False, back_populates=f'map{map_number}')

    def __repr__(self):
        return f'{self.team1} - {self.team2} | Map:{self.map_number}'

    # !add __init__ method!


class TeamLine(Base):
    """
    Сomplex abstraction which contains all maps played between two teams in one event
    store all information about event and team-line odds
    """
    __tablename__ = 'TeamLines'

    id = Column(Integer, primary_key=True, nullable=False)

    group = relationship('Group', backref='teamlines')
    group_id = Column(Integer, ForeignKey('Groups.id'))

    league = relationship('League', backref='teamlines')
    league_ld = Column(Integer, ForeignKey('Leagues.id'))

    map1 = relationship('Map', back_populates='team_line')
    map1_id = Column(Integer, ForeignKey('Maps.id'), nullable=True)

    map2 = relationship('Map', back_populates='team_line')
    map2_id = Column(Integer, ForeignKey('Maps.id'), nullable=True)
    # ??????
    map3 = relationship('Map', back_populates='team_line')
    map3_id = Column(Integer, ForeignKey('Maps.id'), nullable=True)

    map4 = relationship('Map', back_populates='team_line')
    map4_id = Column(Integer, ForeignKey('Maps.id'), nullable=True)

    map5 = relationship('Map', back_populates='team_line')
    map5_id = Column(Integer, ForeignKey('Maps.id'), nullable=True)

    extra_data = Column(JSON)

    def __repr__(self):
        return f'{self.group}, {self.league}:' \
               f' {self.map1.team1} vs {self.map1.team2} (teamline)'

    # !add __init__ method!
