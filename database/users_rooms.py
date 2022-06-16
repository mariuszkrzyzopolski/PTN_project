# from sqlalchemy import Column, ForeignKey, Table
# from sqlalchemy.orm import relationship
#
#
#
# class UsersRooms(Base):
#     __tablename__ = 'users_rooms'
#
#     user_id = Column(ForeignKey('user.id'), primary_key=True)
#     room_id = Column(ForeignKey('room.id'), primary_key=True)
#     user = relationship("User", back_populates="rooms")
#     room = relationship("Room", back_populates="users")
from sqlalchemy import Table, Column, ForeignKey

from database.database import Base

users_rooms = Table(
    "users_rooms",
    Base.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("room_id", ForeignKey("Room.id"), primary_key=True)
)
