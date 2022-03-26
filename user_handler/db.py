import getpass
import os
import csv


class DB:
    def __init__(self, current_dir):
        self.db_path = os.path.join(current_dir, "db.csv")
        if not os.path.exists(self.db_path):
            file = open('db.csv', 'w+')
            file.close()

    def is_exist(self, username, password, check_password=False):
        with open(self.db_path) as db:
            file = csv.reader(db, delimiter=' ', quotechar='|')
            for row in file:
                if check_password:
                    if row[0] == username and row[1] == password:
                        return True
                else:
                    if row[0].lower() == username.lower():
                        return True
        return False

    @staticmethod
    def secure_password(password):
        if len(password) < 6:
            return False
        elif not any(char.isdigit() for char in password):
            return False
        elif not any(char.islower() for char in password):
            return False
        elif not any(char.isupper() for char in password):
            return False
        elif not any(not char.isalnum() for char in password):
            return False
        return True

    def login(self):
        username = input("podaj nazwe uzytkownika: ")
        password = getpass.getpass(prompt="podaj haslo: ")
        if self.is_exist(username, password, True):
            print("Witamy!")
        else:
            print("Niepoprawne dane, sprobuj jeszcze raz")

    def register(self):
        username = input("podaj nazwe uzytkownika: ")
        password = getpass.getpass(prompt="podaj haslo: ")
        second_password = getpass.getpass(prompt="powtorz wpisane haslo: ")
        if password != second_password:
            print("Hasla sie nie zgadzaja")
        elif self.is_exist(username, password):
            print("Zajeta nazwa uzytkownika")
        elif not self.secure_password(password):
            print("Hasło nie jest bezpieczne, stwórz bezpieczne hasło")
        else:
            with open(self.db_path, "a", newline='') as db:
                file = csv.writer(db, delimiter=' ', quotechar='|')
                file.writerow([username, password])

    def list_users(self, mode):
        if mode[3] == "all":
            with open(self.db_path) as db:
                file = csv.reader(db, delimiter=' ', quotechar='|')
                for row in file:
                    print(row[0])
        elif mode[3] == "sort":
            with open(self.db_path) as db:
                file = csv.reader(db, delimiter=' ', quotechar='|')
                users = []
                for row in file:
                    users.append(row[0])
            users.sort()
            for user in users:
                print(user)
        elif mode[3] == "by_letter":
            with open(self.db_path) as db:
                file = csv.reader(db, delimiter=' ', quotechar='|')
                for row in file:
                    if row[0][0] == mode[4]:
                        print(row[0])
        elif mode[3] == "contain":
            with open(self.db_path) as db:
                file = csv.reader(db, delimiter=' ', quotechar='|')
                for row in file:
                    if mode[4] in row[0]:
                        print(row[0])

    def delete_user(self, user):
        list_of_lines = list()
        with open(self.db_path, 'r') as readFile:
            reader = csv.reader(readFile, delimiter=' ', quotechar='|')
            for row in reader:
                list_of_lines.append(row)
                if row[0] == user:
                    list_of_lines.remove(row)
        with open(self.db_path, 'w') as writeFile:
            writer = csv.writer(writeFile, delimiter=' ', quotechar='|')
            writer.writerows(list_of_lines)
