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
DEFAULT_PRODUCT_DETAILS = {
    "title": "No title",
    "description": "No description",
    "price": 0.00
}

buying_router = Router()
db_manager = DatabaseManager('product')


def format_product_details(product: Dict) -> str:
    """
    Formats product details for the user.
    """
    return (
        f"Title: {product.get('title', DEFAULT_PRODUCT_DETAILS['title'])}\n"
        f"Description: {product.get('description', DEFAULT_PRODUCT_DETAILS['description'])}\n"
        f"Price: ${product.get('price', DEFAULT_PRODUCT_DETAILS['price']):.2f}\n"
    )


def generate_image_path(product: Dict) -> str | None:
    """
    Generates the image file path for a product if available.
    """
    img_ref = product.get('img_ref')
    return path.join(IMAGE_DIRECTORY, img_ref) if img_ref else None


async def send_all_products(message: types.Message, products: list) -> None:
    """
    Sends product details and images in bulk.
    """
    for product in products:
        product_details = format_product_details(product)
        image_path = generate_image_path(product)
        await send_product_message(message, product_details, image_path)


async def send_product_message(message: types.Message, product_details: str, image_path: str | None) -> None:
    """
    Sends a single product's message with or without an image.
    """
    if image_path and path.exists(image_path):
        await message.answer_photo(photo=FSInputFile(image_path), caption=product_details)
    else:
        await message.answer(product_details + "\nImage not found.")


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message, state: FSMContext) -> None:
    """
    Handler for the initial buying message. It lists all the products available.
    """
    products = await get_all_products(db_manager)
    if not products:
        await message.answer('No products available.')
        return

    await send_all_products(message, products)
    await message.answer('All products listed above.', reply_markup=inline_buying_menu_kbd())


@buying_router.callback_query(F.data == 'product_buying')
async def handle_the_deal(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handler for dealing with the product-buying process.
    """
    await callback_query.message.answer(
        'Thank you for your purchase! Your balance has been updated.'
    )
    await callback_query.answer()
