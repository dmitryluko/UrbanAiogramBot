from db.db_manager import DatabaseManager, DatabaseError
from models.user import User

import logging

from routers.buying_router import db_manager


def is_user_exists(db_manager, email):
    """fetch_if(self, table: str, condition: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]"""
    users = db_manager.fetch_if("users", f"email='{email}'")
    return len(users) > 0


def add_user(db_manager, username, email, age):
    """Add user to db"""
    try:
        if is_user_exists(email):
            logging.error(f"User with email {email} already exists.")
            return
        user = User(username, email, age)
        db_manager.insert_user(user)
    except DatabaseError as e:
        logging.exception(f"Error adding user: {e}")
