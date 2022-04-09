import bcrypt


def get_last_id(db):
    file = db.read("room")
    list_of_rooms = list(file)
    if len(list_of_rooms) == 0:
        return 0
    else:
        return int(list_of_rooms[-1][0]) + 1


class Room:
    def __init__(self, db, password, owner):
        self.id = get_last_id(db)
        self.password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        self.owner = owner
        self.users = owner
        print(f"New room id: {self.id}")
        file = db.write("room", "a")
        file.writerow([self.id, self.password.decode(), self.owner, self. users])
        db.close()
