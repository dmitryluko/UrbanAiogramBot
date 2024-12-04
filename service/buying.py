import logging

from db.db_manager import DatabaseManager, DatabaseError

logger = logging.getLogger(__name__)


async def get_buying_list():
    return [{'title': f'Product{i}', 'description': f'описание {i}', 'price': i * 100, 'img': f'food_img_{i}.png'} for i
            in range(1, 5)]


async def get_all_products(dmb: DatabaseManager):
    try:
        products = await dmb.fetch_all('products', ['title', 'description', 'price', 'img'])
        return products
    except DatabaseError as e:
        logger.exception(f"Error fetching products: {e}")
        return []
