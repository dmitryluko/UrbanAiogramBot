from os import path
from typing import Dict

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from db.db_manager import DatabaseManager
from models.product import Product
from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_all_products

IMAGE_DIRECTORY = 'assets/images/'

buying_router = Router()
db_manager = DatabaseManager()


def prepare_product_details(product: Dict):
    return (
        f"Title: {product.get('title', 'No title')}\n"
        f"Description: {product.get('description', 'No description')}\n"
        f"Price: ${product.get('price', 0):.2f}\n"
    )


def get_image_path(product):
    if 'img_ref' in product and product['img_ref']:
        return path.join(IMAGE_DIRECTORY, product['img_ref'])
    return None


async def send_product_message(message, product_details, image_path):
    if image_path and path.exists(image_path):
        await message.answer_photo(photo=FSInputFile(image_path), caption=product_details)
    else:
        await message.answer(product_details + "\nImage not found.")


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message, state: FSMContext):
    """
    Handler for the initial buying message. It lists all the products available.
    """
    products = await get_all_products(db_manager)

    for product in products:
        product_details = prepare_product_details(product)
        image_path = get_image_path(product)
        await send_product_message(message, product_details, image_path)

    await message.answer('All products listed above.', reply_markup=inline_buying_menu_kbd())


@buying_router.callback_query(F.data == 'product_buying')
async def handle_the_deal(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Handler for dealing with the product buying process.
    """
    await callback_query.message.answer(
        f'Thank you for your purchase! Your balance has been updated.'
    )
    await callback_query.answer()
