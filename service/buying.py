import logging

from db.db_manager import DatabaseManager, DatabaseError
from service.products import add_base_products

logger = logging.getLogger(__name__)


async def get_all_products(dmb: DatabaseManager):
    try:
        products = await dmb.fetch_all('products', ['id', 'title', 'description', 'price', 'img_ref'])

        if not products:
            add_base_products(dmb)
            logger.info('Base products added')

        return products
    except DatabaseError as e:
        logger.exception(f"Error fetching products: {e}")
        return []
