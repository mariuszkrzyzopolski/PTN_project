import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_database():
    return create_engine('sqlite:///sql.db')


class DB:
    def __init__(self, conn):
        self.conn = conn

    def close(self):
        self.conn.commit()
        self.conn.close()

    def initialize_db(self):
        if os.path.exists("db_user.csv") or os.path.exists("db_room.csv"):
            os.remove("db_user.csv")
            os.remove("db_room.csv")
        Base.metadata.drop_all(self.conn)
        Base.metadata.create_all(self.conn)
