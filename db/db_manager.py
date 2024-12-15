import os
import sqlite3
from typing import Any, Dict, List, Optional

import logging

logging.getLogger().setLevel(logging.INFO)


class DatabaseError(Exception):
    """Custom exception class for database-related errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseManager:
    """
    A class to manage SQLite database operations.

    Attributes:
        db_path (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The SQLite connection object.
        cursor (sqlite3.Cursor): The SQLite cursor object.
    """

    def __init__(self, db_name: str, db_dir: str = 'data') -> None:
        """
        Initializes the DatabaseManager with specified database name and directory.

        Args:
            db_name (str): The name of the SQLite database file.
            db_dir (str): The directory where the database file is located.
        """
        self.db_path: str = os.path.join(db_dir, db_name)
        self.conn: sqlite3.Connection = self._connect_to_db()
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.__db_name = db_name
        self._check_db_exists()

    def __del__(self) -> None:
        """Destructor to close the SQLite connection."""
        if self.conn:
            self.conn.close()
            logging.info('Connection closed successfully.')

    def _connect_to_db(self) -> sqlite3.Connection:
        """
        Connects to the SQLite database, creating the directory if it does not exist.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.OperationalError:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            return sqlite3.connect(self.db_path)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    @staticmethod
    def _row_to_dict(row: tuple, columns: List[str]) -> Dict[str, Any]:
        """
        Converts a row tuple to a dictionary mapping column names to their values.

        Args:
            row (tuple): A tuple representing a row of data.
            columns (List[str]): A list of column names corresponding to the tuple values.

        Returns:
            Dict[str, Any]: A dictionary where keys are column names and values are the corresponding row values.
        """
        return {column: row[idx] for idx, column in enumerate(columns)}

    def insert(self, table: str, column_values: Dict[str, Any]) -> None:
        """
        Inserts a row into the specified table.

        Args:
            table (str): The table name.
            column_values (Dict[str, Any]): A dictionary of column names and values to insert.
        """
        columns = ', '.join(column_values.keys())
        values = tuple(column_values.values())
        placeholders = ", ".join("?" * len(column_values))

        try:
            self.cursor.execute(
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                values
            )
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Insert operation failed: {e.args[0]}")

    async def fetch_all(self, table: str, columns: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches all rows from the specified table.

        Args:
            table (str): The table name.
            columns (List[str]): A list of column names to fetch.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched rows.
        """
        columns_str = ", ".join(columns)
        try:
            self.cursor.execute(f"SELECT {columns_str} FROM {table}")
            rows = self.cursor.fetchall()
            return [self._row_to_dict(row, columns) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Fetch operation failed: {e.args[0]}")

    def fetch_if(self, table: str, condition: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Fetches all rows from the specified table, where condition is True with given columns.

        Args:
            table (str): The table name.
            condition (str): The condition for fetching rows.
            columns (List[str], optional): A list of column names to fetch. Defaults to '*'.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched rows.
        """
        columns_str = '*' if columns is None else ', '.join(columns)
        try:
            self.cursor.execute(f"SELECT {columns_str} FROM {table} WHERE {condition}")
            rows = self.cursor.fetchall()
            col_names = [desc[0] for desc in self.cursor.description]
            return [self._row_to_dict(row, col_names) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Fetch operation with condition failed: {e.args[0]}")

    def delete(self, table: str, row_id: int) -> None:
        """
        Deletes a row from the specified table by its ID.

        Args:
            table (str): The table name.
            row_id (int): The ID of the row to delete.
        """
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Delete operation failed: {e.args[0]}")

    def _get_cursor(self) -> sqlite3.Cursor:
        """
        Returns the cursor object.

        Returns:
            sqlite3.Cursor: The cursor object.
        """
        return self.cursor

    def update(self, table: str, column_values: Dict[str, Any], condition: str) -> None:
        """
        Updates rows in the specified table based on the given condition.

        Args:
            table (str): The table name.
            column_values (Dict[str, Any]): A dictionary of column names and values to update.
            condition (str): The condition for updating rows.
        """
        columns = ', '.join(f"{col} = ?" for col in column_values.keys())
        values = list(column_values.values())
        sql = f"UPDATE {table} SET {columns} WHERE {condition}"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Update operation failed: {e.args[0]}")

    def get_table_size(self, table: str) -> int:
        """
        Returns the number of rows in the table.

        Args:
            table (str): The table name.

        Returns:
            int: The total number of rows.
        """
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise DatabaseError(f"Get table size operation failed: {e.args[0]}")

    def get_column_sum(self, table: str, column: str) -> Optional[float]:
        """
        Returns the sum of a specific column in the specified table.

        Args:
            table (str): The table name.
            column (str): The column name.

        Returns:
            Optional[float]: The sum of the column values, or None if an error occurs.
        """
        try:
            return self.cursor.execute(f"SELECT SUM({column}) FROM {table}").fetchone()[0]
        except sqlite3.Error as e:
            raise DatabaseError(f"Get column sum operation failed: {e.args[0]}")

    def get_column_avg(self, table: str, column: str) -> Optional[float]:
        """
        Returns the average of a specific column in the specified table.

        Args:
            table (str): The table name.
            column (str): The column name.

        Returns:
            Optional[float]: The average of the column values, or None if an error occurs.
        """
        try:
            return self.cursor.execute(f"SELECT AVG({column}) FROM {table}").fetchone()[0]
        except sqlite3.Error as e:
            raise DatabaseError(f"Get column average operation failed: {e.args[0]}")

    def _init_db(self) -> None:
        """
        Initializes the database by executing SQL commands from 'create_users_db.sql' file.
        """
        try:
            print(f'Current Path: {os.getcwd()}')
            with open(f'db/sql/create_{self.__db_name}_db.sql') as fd:
                sql = fd.read()
            self.cursor.executescript(sql)
            self.conn.commit()
            log.info(f'Database {self.__db_name} initialized successfully!')
        except (FileNotFoundError, sqlite3.Error) as e:
            raise DatabaseError(f'Database initialization failed: {e}')

    def _check_db_exists(self) -> None:
        """
        Checks if the required tables exist in the database, and initializes the database if not.
        """
        try:
            self.cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.__db_name.capitalize()}'")
            table_exists = self.cursor.fetchall()
            if not table_exists:
                logging.warning('Table does not exists! ')
                self._init_db()
            else:
                logging.info(f'Database {self.__db_name} exists and checked!')
        except sqlite3.Error as e:
            raise DatabaseError(f"Check database existence operation failed: {e.args[0]}")
