import sqlite3
from sqlite3 import Error


class Database:
    """
    Clase para manejar la conexión a la base de datos SQLite.
    """

    def __init__(self, db_file):
        """
        Inicializa la conexión a la base de datos.

        Args:
            db_file (str): Ruta al archivo de la base de datos.
        """
        self.connection = self.create_connection(db_file)
        self.cursor = self.connection.cursor()

    def create_connection(self, db_file):
        """
        Crea una conexión a la base de datos SQLite.

        Args:
            db_file (str): Ruta al archivo de la base de datos.

        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos.
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self, create_table_sql):
        """
        Crea una tabla en la base de datos.

        Args:
            create_table_sql (str): Sentencia SQL para crear la tabla.
        """
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        self.connection.close()
