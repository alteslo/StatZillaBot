from logging import Logger
import sqlite3
import datetime


class Database():
    """Модель базы данных"""
    def __init__(self, path_to_db="main.db"):
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
            data = connection.fetchone()
        if fetchall:
            data = connection.fetchall()

        connection.close()
        return data

    def create_table_users(self):
        """Создаем структуру базы данных"""
        sql = """
        CREATE TABLE users(
            user_id INT PRIMARY KEY NOT NULL,
            name VARCHAR(150) NOT NULL,
            email VARCHAR(150));
        """
        self.execute(sql, commit=True)

    def add_user(self, user_id: int, name: str, email: str = None):
        """Добавляем нового пользователя"""
        sql = """INSERT INTO users(user_id, name, email) VALUES (?, ?, ?);"""
        parameters = (user_id, name, email)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_users(self):
        sql = """SELECT * FROM users"""
        return self.execute(sql, fetchall=True)
