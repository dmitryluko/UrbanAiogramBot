from aiogram import Router, F, types

from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_buying_list

buying_router = Router()


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message):
    products = await get_buying_list()
    product_list_message = "Available products:\n"

    for product in products:
        product_list_message += (
            f"\nTitle: {product['title']}\n"
            f"Description: {product['description']}\n"
            f"Price: ${product['price']}\n"
            f"Image: {product['img']}\n"
        )

    await message.answer(product_list_message, reply_markup=inline_buying_menu_kbd())
