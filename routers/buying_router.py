from os import path

from aiogram import Router, F, types
from aiogram.types import InputFile, FSInputFile

from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_buying_list

buying_router = Router()


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message):
    products = await get_buying_list()

    for product in products:
        # Prepare the product details message
        product_details = (
            f"Title: {product['title']}\n"
            f"Description: {product['description']}\n"
            f"Price: ${product['price']}\n"
        )

        image_path = path.join('assets/images/', product['img'])

        try:
            await message.answer_photo(photo=FSInputFile(image_path), caption=product_details)
        except FileNotFoundError:
            await message.answer(product_details + "\nImage not found.")

    await message.answer("All products listed above.", reply_markup=inline_buying_menu_kbd())
