from typing import Dict, List, Optional, Tuple, Any
from db.db_manager import DatabaseManager

USER_EMAIL_DOMAIN = '@gmail.com'
INITIAL_BALANCE = 1000
UPDATED_BALANCE = 500


def create_user(i: int) -> Dict[str, Any]:
    """
    Creates a user dictionary.

    Args:
        i (int): An integer index to create unique user data.

    Returns:
        Dict[str, Any]: A dictionary containing user information.
    """
    return {
        'username': f'User{i + 1}',
        'email': f'example{i + 1}{USER_EMAIL_DOMAIN}',
        'age': (i + 1) * 10,
        'balance': INITIAL_BALANCE
    }


def add_users(db_manager: DatabaseManager, num_users: int = 10) -> None:
    """
    Adds a specified number of users to the database.

    Args:
        db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
        num_users (int, optional): The number of users to add. Defaults to 10.
    """
    for i in range(num_users):
        user = create_user(i)
        db_manager.insert(table='users', column_values=user)


def update_alternate_users_balance(db_manager: DatabaseManager) -> None:
    """
    Updates the balance for every alternate user in the database.

    Args:
        db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
    """
    users = db_manager.fetch_all(table='users', columns=['id'])
    for user in users[::2]:
        db_manager.update(table='users', column_values={'balance': UPDATED_BALANCE}, condition=f'id = {user["id"]}')


def delete_every_nth_user(db_manager: DatabaseManager, n: int = 3) -> None:
    """
    Deletes every nth user from the database.

    Args:
        db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
        n (int, optional): Specifies the interval for deletion (every nth user). Defaults to 3.
    """
    user_ids = db_manager.fetch_all(table='users', columns=['id'])
    for user in user_ids[::n]:
        db_manager.delete(table='users', row_id=user['id'])


def fetch_users_not_of_age(db_manager: DatabaseManager, age: int = 60) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches users whose age is not equal to the specified age.

    Args:
        db_manager (DatabaseManager): An instance of DatabaseManager to interact with the database.
        age (int, optional): The age to exclude from the result set. Defaults to 60.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries containing user information.
    """
    return db_manager.fetch_if(
        table='users',
        condition=f'age != {age}',
        columns=['username', 'email', 'age', 'balance']
    )


def print_users(users_list: Optional[List[Dict[str, Any]]]) -> None:
    """
    Prints the user information in the provided list.

    Args:
        users_list (Optional[List[Dict[str, Any]]]): A list of user dictionaries to print.
    """
    if users_list:
        for user in users_list:
            print(
                f'Имя: {user["username"]} | Почта: {user["email"]} | Возраст: {user["age"]} | Баланс: {user["balance"]}')


def main() -> None:
    db_mgr = DatabaseManager()
    add_users(db_mgr)
    update_alternate_users_balance(db_mgr)
    delete_every_nth_user(db_mgr)
    print_users(fetch_users_not_of_age(db_mgr))


if __name__ == '__main__':
    main()
