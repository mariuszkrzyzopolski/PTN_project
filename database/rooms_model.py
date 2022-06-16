from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base
from database.users_rooms import users_rooms


class Room(Base):
    __tablename__ = 'Room'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    owner = Column(Integer, ForeignKey('User.id'))
    topic = Column(String)

    user = relationship("User", back_populates="room")
    users = relationship("User", secondary=users_rooms, back_populates="rooms")
    votes = relationship("Vote", back_populates="room")
