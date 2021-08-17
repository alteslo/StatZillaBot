import sqlite3
import datetime


class Database():
    """Модель базы данных"""
    def __init__(self, path_to_db=r"app\data\main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None,
                fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()

        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        """Создаем структуру базы данных"""
        sql = """
        CREATE TABLE users(
            user_id INT PRIMARY KEY NOT NULL,
            name VARCHAR(150) NOT NULL,
            phone VARCHAR(150));
        """
        self.execute(sql, commit=True)

    def add_user(self, user_id: int, name: str, phone: str = None):
        """Добавляем нового пользователя"""
        sql = """INSERT INTO users(user_id, name, phone) VALUES (?, ?, ?);"""
        parameters = (user_id, name, phone)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        """Возвращает всех пользователей"""
        sql = """SELECT * FROM users"""
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        """Метод используемый как функция с помощью @staticmethod"""
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name=?"
        sql += " AND ".join([f'{item} = ?' for item in parameters])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        """Возвращает пользователя"""
        sql = """SELECT * FROM users WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        """Возвращает количесво пользователей"""
        sql = """SELECT COUNT(*) FROM users"""
        return self.execute(sql, fetchone=True)

    def update_user_phone(self, phone, user_id):
        sql = """UPDATE users SET phone=? WHERE user_id=?"""
        return self.execute(sql, parameters=(phone, user_id), commit=True)

    def delete_users(self):
        sql = """DELETE FROM users"""
        self.execute(sql, commit=True)


db = Database()
