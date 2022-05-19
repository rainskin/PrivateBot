import sqlite3
from sqlite3 import OperationalError


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id) -> bool:
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(result)

    def add_user(self, user_id: int):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

    def set_active(self, user_id: int, active: bool):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM users").fetchall()

    def create_tables(self):
        with self.connection:
            try:
                self.cursor.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, active INTEGER)")
            except OperationalError:
                pass
