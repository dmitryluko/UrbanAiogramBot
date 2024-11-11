# Create Inline Keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu_kbd() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Calculate'),
                KeyboardButton(text='Buy 🪙'),
                KeyboardButton(text='Info'),
            ]
        ],
        resize_keyboard=True,
    )


def inline_menu_kbd() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
                InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'),
            ]
        ]
    )


def inline_buying_menu_kbd() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Product1", callback_data="product_buying"),
        InlineKeyboardButton(text="Product2", callback_data="product_buying"),
        InlineKeyboardButton(text="Product3", callback_data="product_buying"),
        InlineKeyboardButton(text="Product4", callback_data="product_buying"),
    ]
    keyboard = InlineKeyboardMarkup().add(*buttons)
    return keyboard
