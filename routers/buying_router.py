from aiogram import Router, F

buying_router = Router()


@buying_router.message(F.text == 'Buy')
async def buying(message):
    await message.answer('buying')
