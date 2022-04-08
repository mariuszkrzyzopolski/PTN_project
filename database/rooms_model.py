import bcrypt


def get_last_id(db):
    file = db.read("room")
    if len(list(file)) == 0:
        return 0
    else:
        return file[-1][0] + 1


class Room:
    def __init__(self, db, password, owner):
        self.id = get_last_id(db)
        self.password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        self.owner = owner
        self.users = [owner]

        file = db.write("room", "a")
        file.writerow([self.id, self.password, self.owner, self. users])
        db.close()
