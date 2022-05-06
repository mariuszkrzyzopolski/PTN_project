import getpass

import bcrypt

from database.users_model import User


def secure_password(password):
    if len(password) < 6:
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif not any(char.islower() for char in password):
        return False
    elif not any(char.isupper() for char in password):
        return False
    elif not any(not char.isalnum() for char in password):
        return False
    return True


def login(db):
    username = input("username: ")
    password = getpass.getpass(prompt="password: ")
    user = User(username, bytes(password, 'utf-8'))
    if is_exist(user.username, user.password, db, True):
        print(f"Welcome {username}!")
        return username
    else:
        print("Wrong username or password")
        return login(db)


def register(db):
    username = input("username: ")
    password = getpass.getpass(prompt="password: ")
    second_password = getpass.getpass(prompt="repeat password: ")
    user = User(username, bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()))
    if password != second_password:
        print("Passwords are different")
    elif not secure_password(password):
        print("Password is not secure again, try more complex password")
    elif is_exist(user.username, user.password, db):
        print("user already exists")
    else:
        db.cursor.execute(f"INSERT INTO USER VALUES ('{username}' , '{user.password.decode()}')")
    db.close()


def list_users(db, mode):
    if mode[3] == "all":
        db.cursor.execute(f"SELECT username FROM USER")
        data = db.cursor.fetchall()
        for record in data:
            print(record)
        db.close()
    elif mode[3] == "sort":
        db.cursor.execute(f"SELECT username FROM USER ORDER BY username")
        data = db.cursor.fetchall()
        for record in data:
            print(record)
        db.close()
    elif mode[3] == "contain":
        db.cursor.execute(f"SELECT username FROM WHERE username LIKE '%{mode[4]}%'")
        data = db.cursor.fetchall()
        for record in data:
            print(record)
        db.close()


def delete_user(db, user):
    db.cursor.execute(f"DELETE FROM USER WHERE username = '{user}'")
    db.close()


def is_exist(username, password, db, check_password=False):
    db.cursor.execute(f"SELECT username,password FROM USER WHERE username = '{username}'")
    data = db.cursor.fetchall()
    if len(data) != 0:
        if check_password:
            if bcrypt.checkpw(password, bytes(data[1], 'utf-8')):
                return True
        else:
            return True
    return False
