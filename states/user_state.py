from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    """
    UserState class is a subclass of StatesGroup and holds various states related to a user.

    Attributes:
        age(State): Represents the state where the age of the user is stored.
        height(State): Represents the state where the height of the user is stored.
        weight(State): Represents the state where the weight of the user is stored.
    """
    age = State()
    height = State()
    weight = State()
