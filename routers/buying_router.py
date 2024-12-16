from os import path
from typing import Dict, List, Optional
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from db.db_manager import DatabaseManager
from resources.keyboards import inline_buying_menu_kbd
from service.buying import get_all_products

# Constants
IMAGE_DIRECTORY: str = 'assets/images/'
DEFAULT_PRODUCT_DETAILS: Dict[str, str | float] = {
    'title': 'No title',
    'description': 'No description',
    'price': 0.00
}
NO_PRODUCTS_MESSAGE: str = 'No products available.'

# Initialize router and database manager
buying_router: Router = Router()
db_manager: DatabaseManager = DatabaseManager('products')


def generate_image_path(product: Dict) -> Optional[str]:
    """
    Generates the absolute image path for a product if the image reference exists.

    Args:
        product (Dict): Dictionary containing product details including `img_ref`.

    Returns:
        Optional[str]: The absolute image path if `img_ref` exists, else None.
    """
    img_ref: Optional[str] = product.get('img_ref')
    return path.join(IMAGE_DIRECTORY, img_ref) if img_ref else None


async def handle_no_products_message(message: types.Message) -> None:
    """
    Sends a message when there are no products available.

    Args:
        message (types.Message): The message object representing the user's message.
    """
    await message.answer(NO_PRODUCTS_MESSAGE)


async def send_product_message(
        message: types.Message,
        product_details: str,
        image_path: Optional[str]
) -> None:
    """
    Sends a product's details to the user, including an image if available.

    Args:
        message (types.Message): The message object representing the user's message.
        product_details (str): A string containing the product's details.
        image_path (Optional[str]): The file path to the product's image.
    """
    if image_path and path.exists(image_path):
        await message.answer_photo(photo=FSInputFile(image_path), caption=product_details)
    else:
        await message.answer(product_details + "\nImage not found.")


@buying_router.message(F.text == 'Buy')
async def buying(message: types.Message, state: FSMContext) -> None: # TODO: Implement business logic
    """
    Handles the 'Buy' command by retrieving and listing all available products.

    Args:
        message (types.Message): The message object representing the user's message.
        state (FSMContext): The FSM (Finite State Machine) context object for handling states.
    """
    product_list: List[Dict] = await get_all_products(db_manager)

    if not product_list:
        await handle_no_products_message(message)
        return

    # Iterate through products and send product details to the user
    for product in product_list:
        product_details: str = "\n".join([
            f"Title: {product.get('title', DEFAULT_PRODUCT_DETAILS['title'])}",
            f"Description: {product.get('description', DEFAULT_PRODUCT_DETAILS['description'])}",
            f"Price: ${product.get('price', DEFAULT_PRODUCT_DETAILS['price']):.2f}"
        ])
        image_path: Optional[str] = generate_image_path(product)
        await send_product_message(message, product_details, image_path)

    await message.answer('All products listed above.', reply_markup=inline_buying_menu_kbd())


@buying_router.callback_query(F.data == 'product_buying')
async def handle_the_deal(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Handles the callback query when the user confirms a purchase.

    Args:
        callback_query (types.CallbackQuery): The callback query object representing user action.
        state (FSMContext): The FSM (Finite State Machine) context object for handling states.
    """
    await state.clear()
    await callback_query.message.answer(
        'Thank you for your purchase! Your balance has been updated.'
    )
    await callback_query.answer()
