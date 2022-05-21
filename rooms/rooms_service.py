import bcrypt

from database.rooms_model import Room


def create_room(db, password, owner):
    room = Room(password, owner)
    db.cursor.execute(
        f"INSERT INTO ROOM (owner, password, users, topic, votes) VALUES ('{room.owner}', '{room.password.decode()}',"
        f" '{room.users}', '{room.topic}', '{room.votes}')")
    db.cursor.execute("SELECT last_insert_rowid()")
    print(f"New room id: {db.cursor.fetchall()[0][0]}")


def delete_room(db, room_id, user):
    db.cursor.execute(f"DELETE FROM ROOM WHERE owner = '{user}' AND room_id = {room_id}")
    print(f"room {room_id} deleted")


def login_into_room(db, password, room_id):
    db.cursor.execute(f"SELECT users, password FROM ROOM WHERE room_id = '{room_id}'")
    data = db.cursor.fetchall()
    if len(data) != 0:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(data[0][1], 'utf-8')):
            return [True, data]
    return [False]


def join_room(db, room_id, room_password, user):
    is_logged = login_into_room(db, room_password, room_id)
    if is_logged[0]:
        data = is_logged[1]
        if user not in data[0][0].split("/"):
            db.cursor.execute('UPDATE ROOM SET users=? WHERE room_id=?', (f"{data[0][0]}/{user}", room_id))
            print(f"joined into {room_id} room")
        else:
            print("You're already in room")
    else:
        print("wrong password")


def set_topic(db, room_id, room_password, topic):
    is_logged = login_into_room(db, room_password, room_id)
    if is_logged[0]:
        db.cursor.execute('UPDATE ROOM SET topic=?, votes=? WHERE room_id=?', (topic, "", room_id))
        print(f"Topic is {topic} now")
    else:
        print("wrong password")


def vote_for_topic(db, room_id, room_password, vote, user):
    is_logged = login_into_room(db, room_password, room_id)
    if is_logged[0]:
        data = is_logged[1]
        if user in data[0][0].split("/"):
            db.cursor.execute(f"SELECT votes FROM ROOM WHERE room_id = '{room_id}'")
            data = db.cursor.fetchall()
            db.cursor.execute('UPDATE ROOM SET votes=? WHERE room_id=?', (f"{data[0][0]}/{vote}", room_id))
            db.conn.commit()
            db.cursor.execute(f"SELECT votes FROM ROOM WHERE room_id = '{room_id}'")
            data = db.cursor.fetchall()
            print(f"Actual votes {data[0][0]}")
        else:
            print("You are not in the target room")
    else:
        print("wrong password")
