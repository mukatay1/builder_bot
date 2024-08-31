from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import NUMBERS


def get_number_keyboard() -> InlineKeyboardMarkup:
    kb = [InlineKeyboardButton(text=str(num), callback_data=f"number_{i}") for i, num in enumerate(NUMBERS)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[kb])
    return keyboard


