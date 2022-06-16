from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base
from database.users_rooms import users_rooms


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    room = relationship("Room", back_populates="user")
    rooms = relationship("Room", secondary=users_rooms, back_populates="users")
    votes = relationship("Vote", back_populates="user")
