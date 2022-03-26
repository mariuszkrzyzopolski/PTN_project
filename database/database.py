import csv
import os


class DB:
    def __init__(self, current_dir):
        self.db_path = os.path.join(current_dir, "db.csv")
        if not os.path.exists(self.db_path):
            file = open('db.csv', 'w+')
            file.close()

    def read(self):
        db = open(self.db_path)
        return csv.reader(db, delimiter=' ', quotechar='|')