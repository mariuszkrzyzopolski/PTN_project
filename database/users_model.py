import bcrypt


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    def is_exist(self, db, check_password=False):
        file = db.read("user")
        for row in file:
            if check_password:
                if row[0] == self.username and bcrypt.checkpw(bytes(row[1], 'utf-8'), self.password):
                    return True
            else:
                if row[0].lower() == self.username.lower():
                    db.close()
                    return True
        db.close()
        return False
