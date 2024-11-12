from aiogram.fsm.state import StatesGroup, State


class BuyingState(StatesGroup):
    start_deal = State()
    product = State()
