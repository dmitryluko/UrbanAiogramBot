from typing import Union

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from resources.keyboards import inline_menu_kbd
from resources.messages_constants import MIFFLIN_FORMULA_MESSAGE, AGE_PROMPT_MESSAGE, HEIGHT_PROMPT_MESSAGE, \
    WEIGHT_PROMPT_MESSAGE, CALCULATION_ERROR_MESSAGE
from states.user_state import UserState
from utils.calories import calculate_calories

calorie_router = Router()


# Prompt function
async def ask_question(message: types.Message, prompt: str) -> None:
    await message.answer(prompt, reply_markup=ReplyKeyboardRemove())


@calorie_router.message(F.text == 'Calculate')
async def main_menu(message: types.Message) -> None:
    await message.answer("Выберите опцию:", reply_markup=inline_menu_kbd())


@calorie_router.callback_query(F.data == 'formulas')
async def show_formulas(callback_query: types.CallbackQuery) -> None:
    await callback_query.message.answer(MIFFLIN_FORMULA_MESSAGE)


@calorie_router.callback_query(F.data == 'calories')
@calorie_router.message(Command('Calories'))
async def start_calorie_calculation(interaction: Union[types.CallbackQuery, types.Message], state: FSMContext) -> None:
    await state.set_state(UserState.age)
    await ask_question(interaction.message if isinstance(interaction, types.CallbackQuery) else interaction,
                       AGE_PROMPT_MESSAGE)


@calorie_router.message(UserState.age)
async def handle_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await state.set_state(UserState.height)
    await ask_question(message, HEIGHT_PROMPT_MESSAGE)


@calorie_router.message(UserState.height)
async def handle_height(message: types.Message, state: FSMContext) -> None:
    await state.update_data(height=message.text)
    await state.set_state(UserState.weight)
    await ask_question(message, WEIGHT_PROMPT_MESSAGE)


@calorie_router.message(UserState.weight)
async def handle_weight(message: types.Message, state: FSMContext) -> None:
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
