from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.user_state import UserState

calorie_router = Router()

CALCULATION_ERROR_MESSAGE = "Ошибка ввода данных. Пожалуйста, начните заново, введя команду 'Calories'."
AGE_PROMPT_MESSAGE = "Введите свой возраст:"
HEIGHT_PROMPT_MESSAGE = "Введите свой рост:"
WEIGHT_PROMPT_MESSAGE = "Введите свой вес:"


@calorie_router.message(Command('Calories'))
@calorie_router.message(F.text == 'Calories')
async def calorie_start_handler(message: types.Message, state: FSMContext) -> None:
    """
    :param message: The message object that triggered the handler, containing details about the user input.
    :param state: The current state object used to manage the finite state machine (FSM) for user interactions.
    :return: None
    """
    await state.set_state(UserState.age)
    await ask_next_question(message, AGE_PROMPT_MESSAGE)


@calorie_router.message(UserState.age)
async def age_handler(message: types.Message, state: FSMContext) -> None:
    """
    :param message: The message object containing the user's input.
    :param state: The current FSMContext instance, allowing interaction with the user's state.
    :return: None
    """
    await state.update_data(age=message.text)
    await state.set_state(UserState.height)
    await ask_next_question(message, HEIGHT_PROMPT_MESSAGE)


@calorie_router.message(UserState.height)
async def height_handler(message: types.Message, state: FSMContext) -> None:
    """
    :param message: The message received from the user.
    :param state: The current state of the finite state machine context.
    :return: None
    """
    await state.update_data(height=message.text)
    await state.set_state(UserState.weight)
    await ask_next_question(message, WEIGHT_PROMPT_MESSAGE)


@calorie_router.message(UserState.weight)
async def weight_handler(message: types.Message, state: FSMContext):
    """
    :param message: The message object containing user input related to weight.
    :param state: The FSMContext object for managing the state of the conversation.
    :return: None
    """
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


async def ask_next_question(message: types.Message, prompt: str) -> None:
    """
    :param message: The incoming message object from the user, typically of type types.Message.
    :param prompt: The string prompt to be sent back as a response to the user.
    :return: None. This function sends a response message asynchronously to the user.
    """
    await message.answer(
        prompt,
        reply_markup=ReplyKeyboardRemove(),
    )


def calculate_calories(age: int, height: int, weight: int) -> float:
    """
    :param age: The age of the person in years.
    :param height: The height of the person in centimeters.
    :param weight: The weight of the person in kilograms.
    :return: The estimated basal metabolic rate (BMR) for the person in calories per day.
    """
    return 10 * weight + 6.25 * height - 5 * age + 5
