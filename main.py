import asyncio
import logging
import sys
import types
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from dotenv import load_dotenv

from routers.calories_router import calorie_router
from states.user_state import UserState

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

WELCOME_MESSAGE = "Welcome! Type 'Calories' to start the calorie calculation process."

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(calorie_router)


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(WELCOME_MESSAGE)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
