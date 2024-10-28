from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.formatting import Text

from states.user_state import UserState

calorie_router = Router()

CALCULATION_ERROR_MESSAGE = "Ошибка ввода данных. Пожалуйста, начните заново, введя команду 'Calories'."


@calorie_router.message(Command('Calories'))
@calorie_router.message(F.text == 'Calories')
async def calorie_start_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(UserState.age)
    await message.answer(
        "Введите свой возраст:",
        reply_markup=ReplyKeyboardRemove(),
    )


@calorie_router.message(UserState.age)
async def set_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(UserState.height)
    await message.answer(
        "Введите свой рост:",
        reply_markup=ReplyKeyboardRemove(),
    )


@calorie_router.message(UserState.height)
async def set_height(message: types.Message, state: FSMContext) -> None:
    await state.update_data(height=message.text)
    await state.set_state(UserState.weight)
    await message.answer(
        "Введите свой вес:",
        reply_markup=ReplyKeyboardRemove(),
    )


@calorie_router.message(UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        age = int(data['age'])
        height = int(data['height'])
        weight = int(data['weight'])
    except ValueError:
        await message.answer(CALCULATION_ERROR_MESSAGE)
        await state.clear()
        return

    calories = calculate_calories(age, height, weight)

    await message.answer(f"Ваша норма калорий: {calories} калорий в день.")
    await state.clear()


def calculate_calories(age: int, height: int, weight: int) -> float:
    """Calculate daily calorie needs using Mifflin-St Jeor Equation (for men)."""
    return 10 * weight + 6.25 * height - 5 * age + 5
