import asyncio
import logging
import sys
import types
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from dotenv import load_dotenv

from recources.keyboards import main_menu_kbd
from routers.buying_router import buying_router
from routers.calories_router import calorie_router
from routers.errors_router import errors_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(

    calorie_router,
    buying_router,
    errors_router,
)


@dp.message(CommandStart())
async def start_handler(message: Message):
    """
    :param message: The incoming message object containing details such as the message text, sender info, and more.
    :return: Sends a welcome message in response to the start command.
    """
    welcome_message = f"👋 Welcome, user {message.from_user.full_name}! Type 'Calories' to start the calorie calculation process."
    await message.answer(welcome_message)

    await message.answer(
        'Выберите нужное: ',
        reply_markup=main_menu_kbd()
    )


async def main() -> None:
    """
    Initializes and starts the Telegram bot polling.

    :return: None
    """
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
