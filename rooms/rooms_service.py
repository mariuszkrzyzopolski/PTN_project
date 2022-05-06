import getpass

import bcrypt

from database.rooms_model import Room


def create_room(db, owner):
    password = getpass.getpass(prompt="password: ")
    room = Room(db, password, owner)
    db.cursor.execute(f"INSERT INTO ROOM VALUES ('{room.owner}', '{room.password.decode()}', '{room.users}',"
                      f" '{room.topic}')")
    db.close()


def delete_room(db, room_id, user):
    db.cursor.execute(f"DELETE FROM ROOM WHERE owner = '{user}' AND id = {room_id}")
    db.close()


def join_room(db, room_id, user):
    password = getpass.getpass(prompt="password: ")
    db.cursor.execute(f"SELECT users, password FROM ROOM WHERE id = '{room_id}'")
    data = db.cursor.fetchall()
    if len(data) != 0:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(data[1], 'utf-8')):
            if user not in data[0].split("/"):
                db.cursor.execute('UPDATE ROOM SET user=? WHERE id=?', (data[0] + f"/{user}", room_id))
                print(f"joined into {room_id} room")
            else:
                print("You're already in room")


