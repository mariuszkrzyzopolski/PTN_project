import bcrypt

from database.users_model import User
from errors import WrongInputException, ExistingUserException, PasswordComplexException


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


def login(db, username, password):
    user = User(username, bytes(password, 'utf-8'))
    if is_exist(user.username, user.password, db, True):
        print(f"Welcome {username}!")
        return user
    else:
        raise WrongInputException("Wrong login/password")


def register(db, username, password):
    user = User(username, bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt()))
    if not secure_password(password):
        raise PasswordComplexException("Password must be more secure")
    elif is_exist(user.username, user.password, db):
        raise ExistingUserException("User already exist")
    else:
        db.cursor.execute(f"INSERT INTO USER (username, password) VALUES ('{username}' , '{user.password.decode()}')")


def list_users(db, mode):
    if mode == "all":
        db.cursor.execute(f"SELECT username FROM USER")
        data = db.cursor.fetchall()
        result = []
        for record in data:
            json_record = {"username": record[0]}
            result.append(json_record)
            print(json_record)
        return result

    elif mode == "sort":
        db.cursor.execute(f"SELECT username FROM USER ORDER BY username")
        data = db.cursor.fetchall()
        result = []
        for record in data:
            json_record = {"username": record[0]}
            result.append(json_record)
            print(json_record)
        return result

    elif mode == "contain":
        db.cursor.execute(f"SELECT username FROM WHERE username LIKE '%{mode[4]}%'")
        data = db.cursor.fetchall()
        result = []
        for record in data:
            json_record = {"username": record[0]}
            result.append(json_record)
            print(json_record)
        return result


def delete_user(db, user):
    db.cursor.execute(f"DELETE FROM USER WHERE username = '{user}'")
    print(f"user {user} deleted")


def is_exist(username, password, db, check_password=False):
    db.cursor.execute(f"SELECT username,password FROM USER WHERE username = '{username}'")
    data = db.cursor.fetchall()
    if len(data) != 0:
        if check_password:
            if bcrypt.checkpw(password, bytes(data[0][1], 'utf-8')):
                return True
        else:
            return True
    return False
