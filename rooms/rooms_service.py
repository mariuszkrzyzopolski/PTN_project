import bcrypt
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from database.rooms_model import Room
from database.users_model import User
from database.vote_model import Vote


def create_room(db, password, owner, name):
    with Session(db.conn) as session:
        hash_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        q = select(User).filter_by(username=owner)
        user = session.execute(q).first()
        session.add(Room(name=name, owner=owner, password=hash_password, topic="", users=[user[0]]))
        session.commit()
        print("New room create")


def is_owner(db, room_id, user):
    with Session(db.conn) as session:
        q = select(Room).filter_by(id=room_id, owner=user)
        room = session.execute(q).all()
        return room[0]


def joined_rooms(db, user):
    result_rooms = []
    with Session(db.conn) as session:
        q = select(Room).join(User.rooms).where(User.username == user)
        rooms = session.execute(q).all()
        for room in rooms:
            result_rooms.append({"name": room[0].name, "id": room[0].id, "owner": room[0].owner})
    return result_rooms


def delete_room(db, room_id, user):
    with Session(db.conn) as session:
        q = select(User.id).filter_by(username=user)
        user = session.execute(q).first()
        q = select(Room).filter_by(owner=user[0], id=room_id)
        data = session.execute(q).first()
        session.delete(data[0])
        session.commit()
        print(f"room {room_id} deleted")


def get_users_from_room(db, room_id):
    with Session(db.conn) as session:
        q = select(User).join(Room.users).where(Room.id == room_id)
        data = session.execute(q).all()
        return data


def login_into_room(db, password, room_id):
    user = get_users_from_room(db, room_id)
    if user:
        if bcrypt.checkpw(bytes(password, 'utf-8'), user[0][0].password):
            return True
    return False


def join_room(db, room_id, room_password, user):
    is_logged = login_into_room(db, room_password, room_id)
    if is_logged:
        users = get_users_from_room(db, room_id)
        if user not in users[0]:
            with Session(db.conn) as session:
                q = select(Room).filter_by(id=room_id)
                data = session.execute(q).first()
                q = select(User).filter_by(username=user)
                user = session.execute(q).first()
                data[0].users.append(user[0])
                session.commit()
            print(f"joined into {room_id} room")
        else:
            print("You're already in room")
    else:
        print("wrong password")


def set_topic(db, room_id, topic, user):
    if is_owner(db, room_id, user):
        with Session(db.conn) as session:
            session.query(Room).filter(Room.id == room_id).update({"topic": topic})
            session.query(Vote).filter(Vote.room_id == room_id).delete()
            print(f"Topic is {topic} now")
            session.commit()
            return {"id": room_id, "topic": topic}
    else:
        print("Not Owner!")


def vote_for_topic(db, room_id, vote, user):
    data = get_users_from_room(db, room_id)
    if data:
        with Session(db.conn) as session:
            q = select(User).filter_by(username=user)
            user = session.execute(q).first()
            stmt = insert(Vote).values(
                user_id=user[0].id,
                room_id=room_id,
                value=vote
            )
            session.execute(stmt)
            session.commit()

    else:
        print("You are not in the target room")


def get_votes(db, room_id, user):
    data = get_users_from_room(db, room_id)
    if data:
        with Session(db.conn) as session:
            q = select(Vote.value, Vote.user_id).join(Room.votes).where(Vote.room_id == room_id)
            data = session.execute(q).all()
            print([{'username': user, 'value': vote} for vote, user in data])
            if data:
                return [{'username': user, 'value': vote} for vote, user in data]
            else:
                return [{}]


def get_room(db, room_id):
    with Session(db.conn) as session:
        q = select(Room.users).filter_by(id=room_id)
        data = session.execute(q).first()
        return data[0]
