import sqlite3
from sqlite3 import Error


class Database:
    """
    Class to handle the connection to the SQLite database.
    """

    def __init__(self, db_file) -> None:
        """
        Initializes the connection to the database.

        Args:
            db_file (str): Path to the database file.
        """
        # Create a connection to the database
        self.connection = self.create_connection(db_file)

        # Create a cursor for the connection
        self.cursor = self.connection.cursor()

    def create_connection(self, db_file) -> sqlite3.Connection:
        """
        Creates a connection to the SQLite database.

        Args:
            db_file (str): Path to the database file.

        Returns:
            sqlite3.Connection: Connection object to the database.
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            # Print the error message if connection fails
            print(e)
        return conn

    def create_table(self, create_table_sql) -> None:
        """
        Creates a table in the database.

        Args:
            create_table_sql (str): SQL statement to create the table.
        """
        try:
            self.cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def close(self) -> None:
        """
        Closes the active connection to the SQLite database.
        """
        self.connection.close()
