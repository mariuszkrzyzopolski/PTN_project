import getpass

import bcrypt

from database.rooms_model import Room


def create_room(db, owner):
    password = getpass.getpass(prompt="password: ")
    return Room(db, password, owner)


def delete_room(db, room_id, user):
    list_of_lines = list()
    file = db.read("room")
    for row in file:
        list_of_lines.append(row)
        if row[0] == room_id and row[2] == user:
            list_of_lines.remove(row)
            print(f"room {room_id} deleted")
    file = db.write("room", "w+")
    file.writerows(list_of_lines)


def join_room(db, room_id, user):
    list_of_lines = list()
    password = getpass.getpass(prompt="password: ")
    file = db.read("room")
    for row in file:
        list_of_lines.append(row)
        if row[0] == room_id and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(row[1], 'utf-8')):
            if user not in row[3].split("/"):
                row[3] = row[3] + f"/{user}"
                print(f"joined into {room_id} room")
            else:
                print("You're already in room")
    file = db.write("room", "w+")
    file.writerows(list_of_lines)
