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
    if user.is_exist(db, True):
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
    elif user.is_exist(db):
        print("user already exists")
    else:
        file = db.write("user", "a")
        file.writerow([username, user.password.decode()])
        db.close()


def list_users(db, mode):
    if mode[3] == "all":
        file = db.read("user")
        for row in file:
            print(row[0])
        db.close()
    elif mode[3] == "sort":
        file = db.read("user")
        users = []
        for row in file:
            users.append(row[0])
        users.sort()
        for user in users:
            print(user)
        db.close()
    elif mode[3] == "by_letter":
        file = db.read("user")
        for row in file:
            if row[0][0] == mode[4]:
                print(row[0])
        db.close()
    elif mode[3] == "contain":
        file = db.read("user")
        for row in file:
            if mode[4] in row[0]:
                print(row[0])
        db.close()


def delete_user(db, user):
    list_of_lines = list()
    file = db.read("user")
    for row in file:
        list_of_lines.append(row)
        if row[0] == user:
            list_of_lines.remove(row)
    file = db.write("user", "w+")
    file.writerows(list_of_lines)
