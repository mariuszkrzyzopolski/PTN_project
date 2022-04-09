import csv
import os


class DB:
    def __init__(self, current_dir):
        self.db_user_path = os.path.join(current_dir, "db_user.csv")
        if not os.path.exists(self.db_user_path):
            self.current_file = open(self.db_user_path, 'w+')
            self.current_file.close()

        self.db_room_path = os.path.join(current_dir, "db_room.csv")
        if not os.path.exists(self.db_room_path):
            self.current_file = open(self.db_room_path, 'w+')
            self.current_file.close()

    def read(self, table):
        if table == "user":
            self.current_file = open(self.db_user_path)
            return csv.reader(self.current_file, delimiter=' ', quotechar='|')
        elif table == "room":
            self.current_file = open(self.db_room_path)
            return csv.reader(self.current_file, delimiter=' ', quotechar='|')

    def write(self, table, mode):
        if table == "user":
            self.current_file = open(self.db_user_path, mode, newline='')
            return csv.writer(self.current_file, delimiter=' ', quotechar='|')
        elif table == "room":
            self.current_file = open(self.db_room_path, mode, newline='')
            return csv.writer(self.current_file, delimiter=' ', quotechar='|')

    def close(self):
        self.current_file.close()
