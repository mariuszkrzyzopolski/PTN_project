import bcrypt


class Room:
    def __init__(self, password, owner):
        self.password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
        self.owner = owner
        self.topic = ""
        self.users = owner
        self.votes = ""
