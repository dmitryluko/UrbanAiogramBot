from os import path
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_buying_list
from states.buying_state import BuyingState

buying_router = Router()


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message, state: FSMContext):
    """
    Handler for the initial buying message. It lists all the products available.
    """
    products = await get_buying_list()
    for product in products:
        # Prepare the product details message
        product_details = (
            f"Title: {product['title']}\n"
            f"Description: {product['description']}\n"
            f"Price: ${product['price']}\n"
        )
        image_path = path.join('assets/images/', product['img'])
        if path.exists(image_path):
            await message.answer_photo(photo=FSInputFile(image_path), caption=product_details)
        else:
            await message.answer(product_details + "\nImage not found.")
    await message.answer("All products listed above.", reply_markup=inline_buying_menu_kbd())


@buying_router.message(F.data == 'product_buying')
async def start_deal(message: types.Message, state: FSMContext):
    """
    Handler for starting a deal after listing all products.
    """
    await state.set_state(BuyingState.product)


@buying_router.message(BuyingState.product)
async def handle_the_deal(message: types.Message, state: FSMContext):
    """
    Handler for dealing with the product buying process.
    """
    # Retrieve product information from state
    product_data = await state.get_data()
    product_details = product_data.get('product_details', 'No product details available.')
    await state.clear()
    await message.answer(
        f"Thank you for your purchase! Your balance has been updated.\n\nProduct Information:\n{product_details}"
    )
