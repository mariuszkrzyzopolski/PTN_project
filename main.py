import os
import sys
from user_handler.db import DB


def run():
    choice = sys.argv[1]
    db = DB(os.path.dirname(os.path.realpath(__file__)))
    if choice == "login":
        db.login()
        if sys.argv[2] == "list_users":
            db.list_users(sys.argv)
        elif sys.argv[2] == "delete_user":
            db.delete_user(sys.argv[3])
    elif choice == "register":
        db.register()
    else:
        print("Podales nieprawidlowe dzialanie, sprobuj jeszcze raz")
        exit()


if __name__ == '__main__':
    run()
