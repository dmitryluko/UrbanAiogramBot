from db.db_manager import DatabaseManager, DatabaseError

import logging

DEFAULT_BALANCE = 1000


def is_user_exists(db_manager: DatabaseManager, username: str) -> bool:
    """
    :param db_manager: The database manager instance used to interact with the database.
    :param username: The username of the user to check for existence in the database.
    :return: A boolean value indicating whether the user exists (True) or not (False).
    """
    users = db_manager.fetch_if('users', f'username="{username}"')
    return len(users) > 0


def log_user_addition(username: str, email: str) -> None:
    """
    :param username: The username of the new user being added.
    :param email: The email address of the new user being added.
    :return: None
    """
    logging.info(f'New User {username} with email: {email} added.')


def add_user(database, username: str, email: str, age: int) -> bool:
    """
    :param database: The database instance used to interact with the 'users' table.
    :param username: The username of the new user to be added.
    :param email: The email address of the new user to be added.
    :param age: The age of the new user to be added.
    :return: True if the user was successfully added to the database, otherwise False.
    """
    try:
        column_values = {
            'username': username,
            'email': email,
            'age': age,
            'balance': DEFAULT_BALANCE
        }
        database.insert('users', column_values)
        log_user_addition(username, email)
        return True
    except DatabaseError as e:
        logging.exception(f"Error adding user: {e}")
        return False
