import getpass

from database.rooms_model import Room


def create_room(db, owner):
    password = getpass.getpass(prompt="podaj haslo: ")
    return Room(db, password, owner)
