import os
import sys
from database.database import DB
from users.users_service import login, list_users, delete_user, register


def run():
    choice = sys.argv[1]
    db = DB(os.path.dirname(os.path.realpath(__file__)))
    if choice == "login":
        login(db.db_path)
        if sys.argv[2] == "list_users":
            list_users(db.db_path, sys.argv)
        elif sys.argv[2] == "delete_user":
            delete_user(db.db_path, sys.argv[3])
    elif choice == "register":
        register(db.db_path)
    else:
        print("Podales nieprawidlowe dzialanie, sprobuj jeszcze raz")
        exit()


if __name__ == '__main__':
    run()
