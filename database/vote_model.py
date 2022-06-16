from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Vote(Base):
    __tablename__ = 'Vote'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    room_id = Column(Integer, ForeignKey('Room.id'))
    value = Column(String)

    user = relationship("User", back_populates="votes")
    room = relationship("Room", back_populates="votes")
