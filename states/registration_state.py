from aiogram.fsm.state import StatesGroup, State


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
