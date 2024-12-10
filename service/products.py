from models.product import Product

from db.db_manager import DatabaseManager


def add_product(db_manager: DatabaseManager, product: Product) -> None:
    column_values = {

        'title': product.title,
        'price': product.price,
        'description': product.description,
        'img_ref': product.img_ref,

    }

    db_manager.insert("products", column_values)


def add_base_products(db_manager: DatabaseManager):
    for idx in range(1, 5):
        product = Product(
            title=f'Product {idx}',
            price=idx * 10,
            description=f'Product {idx} description',
            img_ref=f'food_img_{idx}.png'
        )
        add_product(db_manager, product)
