import os
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
        if os.path.exists("db_user.csv") or os.path.exists("db_room.csv"):
            os.remove("db_user.csv")
            os.remove("db_room.csv")
        self.cursor.execute('''
            CREATE TABLE if not exists user (
                user_id integer PRIMARY KEY AUTOINCREMENT,
                username text NOT NULL UNIQUE,
                password text NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE if not exists room (
                room_id integer PRIMARY KEY AUTOINCREMENT,
                password text NOT NULL,
                owner text NOT NULL,
                topic text NOT NULL,
                users text NOT NULL,
                votes text NOT NULL
            )
        ''')
        self.conn.commit()
