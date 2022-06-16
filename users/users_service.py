import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

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
    user = is_exist(username, password, db, True)
    if user:
        print(f"Welcome {username}!")
        return user
    else:
        raise WrongInputException("Wrong login/password")


def register(db, username, password):
    hash_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    if not secure_password(password):
        raise PasswordComplexException("Password must be more secure")
    elif is_exist(username, hash_password, db):
        raise ExistingUserException("User already exist")
    else:
        with Session(db.conn) as session:
            session.add(User(username=username, password=hash_password))
            session.commit()


def list_users(db, mode):
    if mode == "all":
        with Session(db.conn) as session:
            q = select(User.username)
            data = session.execute(q).all()
            result = []
            for record in data:
                json_record = {"username": record[0]}
                result.append(json_record)
            return result


def delete_user(db, user):
    with Session(db.conn) as session:
        q = select(User).filter_by(username=user)
        data = session.execute(q).first()
        session.delete(data[0])
        session.commit()
        print(f"user {user} deleted")


def is_exist(username, password, db, check_password=False):
    with Session(db.conn) as session:
        q = select(User).filter_by(username=username)
        data = session.execute(q).first()
        if data:
            if check_password:
                if bcrypt.checkpw(password.encode("utf-8"), data[0].password):
                    return data[0]
            else:
                return True
        return False
