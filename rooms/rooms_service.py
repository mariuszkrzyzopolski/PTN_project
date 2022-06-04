import bcrypt

from database.rooms_model import Room


def create_room(db, password, owner, name):
    room = Room(password, owner, name)
    db.cursor.execute(
        f"INSERT INTO ROOM (owner, password, users, topic, votes) VALUES ('{room.owner}', '{room.password.decode()}',"
        f" '{room.users}', '{room.topic}', '{room.votes}')")
    db.conn.commit()
    db.cursor.execute("SELECT last_insert_rowid()")
    print(f"New room id: {db.cursor.fetchall()[0][0]}")


def is_owner(db, room_id, user):
    db.cursor.execute(f"SELECT room_id from room WHERE owner = '{user}' AND room_id = '{room_id}'")
    return len(db.cursor.fetchall()) != 0


def joined_rooms(db, user):
    result_rooms = []
    db.cursor.execute(f"SELECT topic, room_id, owner from room WHERE owner LIKE '%{user}%'")
    rooms = db.cursor.fetchall()
    for room in rooms:
        result_rooms.append({"name": room[0], "id": room[1], "owner": room[2]})
    return result_rooms


def delete_room(db, room_id, user):
    db.cursor.execute(f"DELETE FROM ROOM WHERE owner = '{user}' AND room_id = {room_id}")
    db.conn.commit()
    print(f"room {room_id} deleted")


def get_users_from_room(db, room_id):
    db.cursor.execute(f"SELECT users, password FROM ROOM WHERE room_id = '{room_id}'")
    data = db.cursor.fetchall()
    return data


def login_into_room(db, password, room_id):
    data = get_users_from_room(db, room_id)
    if len(data) != 0:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(data[0][1], 'utf-8')):
            return True
    return False


def join_room(db, room_id, room_password, user):
    is_logged = login_into_room(db, room_password, room_id)
    if is_logged:
        data = get_users_from_room(db, room_id)
        if user not in data[0][0].split("/"):
            db.cursor.execute('UPDATE ROOM SET users=? WHERE room_id=?', (f"{data[0][0]}/{user}", room_id))
            db.conn.commit()
            print(f"joined into {room_id} room")
        else:
            print("You're already in room")
    else:
        print("wrong password")


# TODO change room password and return full room object
def set_topic(db, room_id, topic, user):
    if is_owner(db, room_id, user):
        db.cursor.execute('UPDATE ROOM SET topic=?, votes=? WHERE room_id=?', (topic, "", room_id))
        print(f"Topic is {topic} now")
        db.conn.commit()
        return {"id": room_id, "topic": topic}
    else:
        print("wrong password")


def vote_for_topic(db, room_id, vote, user):
    data = get_users_from_room(db, room_id)
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


def get_votes(db, room_id, user):
    data = get_users_from_room(db, room_id)
    if user in data[0][0].split("/"):
        db.cursor.execute(f"SELECT users, votes FROM ROOM WHERE room_id = '{room_id}'")
        data = db.cursor.fetchall()
        return [{'username': username, 'value': vote} for username, vote in zip(data[0][1].split("/"),
                                                                                data[0][1].split("/"))]


def get_room(db, room_id):
    db.cursor.execute(f"SELECT room_id, topic, users FROM ROOM WHERE room_id = '{room_id}'")
    room = db.cursor.fetchall()
    users = [{'username': user} for user in room[0][2].split("/")]
    return [{"name": "new", "id": room[0][0], "topic": room[0][1], "users": users}]
