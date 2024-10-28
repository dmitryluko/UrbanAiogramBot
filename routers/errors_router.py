from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardRemove, Message

errors_router = Router()


@errors_router.message()
async def error_handler(message: Message):
    await message.answer(f'Error , unrecognized message : {message.text}')
