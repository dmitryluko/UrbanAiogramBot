from typing import Dict

from db.db_manager import DatabaseManager


def add_10_users(db_manager: DatabaseManager):
    for i in range(10):
        username = f'User{i + 1}'
        email = f'example{i + 1}@gmail.com'
        age = (i + 1) * 10
        balance = 1000

        column_values: Dict[str, any] = {
            'username': username,
            'email': email,
            'age': age,
            'balance': balance
        }

        db_manager.insert(table='users', column_values=column_values)


def update_balance(db_manager: DatabaseManager):
    users = db_manager.fetch_all(table='users', columns=['id'])

    for user_id in users[1::2]:
        db_manager.update(table='users', column_values={'balance': 500}, condition=f'id = {user_id["id"]}')


def delete_every_3rd_user(db_manager):
    users = db_manager.fetch_all(table='users', columns=['id'])

    for user_id in users[1::3]:
        db_manager.delete(table='users',row_id=user_id['id'])


def main():
    db_manager = DatabaseManager()

    add_10_users(db_manager)
    update_balance(db_manager)
    delete_every_3rd_user(db_manager)


if __name__ == '__main__':
    main()
