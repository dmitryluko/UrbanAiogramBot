from os import path
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_buying_list

IMAGE_DIRECTORY = 'assets/images/'

buying_router = Router()


def prepare_product_details(product):
    return (
        f"Title: {product['title']}\n"
        f"Description: {product['description']}\n"
        f"Price: ${product['price']}\n"
    )


def get_image_path(product):
    if 'img' in product and product['img']:
        return path.join(IMAGE_DIRECTORY, product['img'])
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
    products = await get_buying_list()

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
