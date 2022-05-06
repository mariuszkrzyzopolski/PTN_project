import sqlite3


def get_database():
    return sqlite3.connect('sql.db')


class DB:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def initialize_db(self):
        pass

