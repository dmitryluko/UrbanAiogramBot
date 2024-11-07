import os
from typing import Dict, List, Tuple, Optional
import sqlite3


class DatabaseManager:
    """
    A class to manage SQLite database operations.

    Attributes:
        db_path (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The SQLite connection object.
        cursor (sqlite3.Cursor): The SQLite cursor object.
    """

    def __init__(self, db_name: str = 'not_telegram.db', db_dir: str = 'data') -> None:
        """
        Initializes the DatabaseManager with specified database name and directory.

        Args:
            db_name (str): The name of the SQLite database file.
            db_dir (str): The directory where the database file is located.
        """
        self.db_path = os.path.join(db_dir, db_name)
        self.conn = self._connect_to_db()
        self.cursor = self.conn.cursor()
        self._check_db_exists()

        def __del__(self):
            """
            Destructor to close the SQLite connection.
            """
            if self.conn:
                self.conn.close()

    def _connect_to_db(self) -> sqlite3.Connection:
        """
        Connects to the SQLite database, creating the directory if it does not exist.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.OperationalError:
            os.mkdir(os.path.dirname(self.db_path))
            return sqlite3.connect(self.db_path)

    def insert(self, table: str, column_values: Dict[str, any]) -> None:
        """
        Inserts a row into the specified table.

        Args:
            table (str): The table name.
            column_values (Dict[str, any]): A dictionary of column names and values to insert.
        """
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))

        self.cursor.executemany(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            values
        )
        self.conn.commit()

    def fetch_all(self, table: str, columns: List[str]) -> List[Dict[str, any]]:
        """
        Fetches all rows from the specified table.

        Args:
            table (str): The table name.
            columns (List[str]): A list of column names to fetch.

        Returns:
            List[Dict[str, any]]: A list of dictionaries representing the fetched rows.
        """
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []

        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)

        return result

    def delete(self, table: str, row_id: int) -> None:
        """
        Deletes a row from the specified table by its ID.

        Args:
            table (str): The table name.
            row_id (int): The ID of the row to delete.
        """
        self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
        self.conn.commit()

    def get_cursor(self) -> sqlite3.Cursor:
        """
        Returns the cursor object.

        Returns:
            sqlite3.Cursor: The cursor object.
        """
        return self.cursor

    def update(self, table: str, column_values: Dict[str, any], condition: str) -> None:
        """
        Updates rows in the specified table based on the given condition.

        Args:
            table (str): The table name.
            column_values (Dict[str, any]): A dictionary of column names and values to update.
            condition (str): The condition for updating rows.
        """
        columns = ', '.join(f"{col} = ?" for col in column_values.keys())
        values = list(column_values.values())

        sql = f"UPDATE {table} SET {columns} WHERE {condition}"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def _init_db(self) -> None:
        """
        Initializes the database by executing SQL commands from 'createdb.sql' file.
        """
        with open('createdb.sql') as fd:
            sql = fd.read()

        self.cursor.executescript(sql)
        self.conn.commit()

    def _check_db_exists(self) -> None:
        """
        Checks if the required tables exist in the database, and initializes the database if not.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
        table_exists = self.cursor.fetchall()

        if not table_exists:
            self._init_db()
