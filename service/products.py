from models.product import Product

from db.db_manager import DatabaseManager


def add_product(db_manager: DatabaseManager, product: Product) -> None:
    column_values = {
        "title": product.title,
        "price": product.price,
        "description": product.description

    }
    db_manager.insert("products", column_values)

def add_base_products(db_manager: DatabaseManager):
    products = []


