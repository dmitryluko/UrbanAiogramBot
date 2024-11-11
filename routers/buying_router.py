from aiogram import Router, F

buying_router = Router()


@buying_router.message(F.Text == 'buy')
async def buying(message):
    await message.answer('buying')
