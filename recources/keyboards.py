# Create Inline Keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_menu_kbd() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
                InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'),
            ]
        ]
    )
