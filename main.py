import os
import sys
from database.database import DB
from rooms.rooms_service import create_room
from users.users_service import login, list_users, delete_user, register


def run():
    choice = sys.argv[1]
    db = DB(os.path.dirname(os.path.realpath(__file__)))
    if choice == "login":
        username = login(db)
        if sys.argv[2] == "list_users":
            list_users(db, sys.argv)
        elif sys.argv[2] == "delete_user":
            delete_user(db, sys.argv[3])
        elif sys.argv[2] == "create_room":
            create_room(db, username)
    elif choice == "register":
        register(db)
    else:
        print("Podales nieprawidlowe dzialanie, sprobuj jeszcze raz")
        exit()


if __name__ == '__main__':
    run()
