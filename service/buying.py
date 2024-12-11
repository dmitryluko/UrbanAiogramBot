import logging
from db.db_manager import DatabaseManager, DatabaseError
from service.products import add_base_products

logger = logging.getLogger(__name__)

PRODUCTS_TABLE = 'products'
PRODUCTS_COLUMNS = ['id', 'title', 'description', 'price', 'img_ref']


async def handle_empty_products(db_manager: DatabaseManager):
    """Handles the scenario when no products are present in the database."""
    add_base_products(db_manager)
    logger.info('No products found. Base products have been added.')


async def get_all_products(db_manager: DatabaseManager):
    """Fetches all products from the database."""
    try:
        products = await db_manager.fetch_all(PRODUCTS_TABLE, PRODUCTS_COLUMNS)
        if not products:
            await handle_empty_products(db_manager)
        return products
    except DatabaseError as e:
        logger.exception(f"Error fetching products: {e}")
        return []
