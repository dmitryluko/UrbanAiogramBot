from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
