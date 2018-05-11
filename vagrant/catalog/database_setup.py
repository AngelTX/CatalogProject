import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)

class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="game")

    @property
    def serialize(self):
        return{
            'name': self.name,
            'id': self.id,
        }

class Tournament(Base):
    __tablename__ = 'tournament'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    location = Column(String(250))
    startDate = Column(String(250))
    endDate = Column(String(250))
    gameID = Column(Integer, ForeignKey('game.id'))
    game = relationship(Game)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="tournament")

    @property
    def serialize(self):
        return{
        'name': self.name,
        'id': self.id,
        'description': self.description,
        'location': self.location,
        'startDate': self.startDate,
        'endDate': self.endDate
        }

engine = create_engine('postgresql://catalog:udacity@localhost/catalog')

Base.metadata.create_all(engine)
