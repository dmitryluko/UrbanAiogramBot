from db.db_manager import DatabaseManager


def get_total_balance(db_manager: DatabaseManager, table: str = 'users') -> float | None:
    return db_manager.get_column_sum(
        table=table,
        column='balance')


def get_average_balance(db_manager: DatabaseManager, table: str = 'users') -> float:
    return db_manager.get_column_avg(
        table=table,
        column='balance'
    )
