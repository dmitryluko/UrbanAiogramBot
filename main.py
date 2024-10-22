import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    :param message:
    """

    logging.info('Command /start handler executing ')
    await message.answer(f'Привет! Я бот помогающий твоему здоровью.')


@dp.message()
async def all_message(message: Message) -> None:
    """
    All messages handler
    :param message:
    """

    logging.info('All message handler executing ')
    await message.answer(
        html.quote('Введите команду /start, чтобы начать общение.'),
        parse_mode=ParseMode.HTML,
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
