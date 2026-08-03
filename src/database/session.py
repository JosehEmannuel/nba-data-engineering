from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.database.connection import get_connection


class DatabaseSession:
    """
    Gerencia uma conexão única com o banco de dados durante
    toda a execução de um pipeline.
    """

    def __init__(self):

        self.connection: MySQLConnection = get_connection()

        self.cursor: MySQLCursor = self.connection.cursor()

    def commit(self):

        self.connection.commit()

    def rollback(self):

        self.connection.rollback()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:

            self.commit()

        else:

            self.rollback()

        self.close()
