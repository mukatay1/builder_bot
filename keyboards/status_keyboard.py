from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import STATUS


def get_status_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text=supervisor, callback_data=f"status_{i}")] for i, supervisor in enumerate(STATUS)]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard


def get_second_status_keyboard() -> InlineKeyboardMarkup:
    kb = [[InlineKeyboardButton(text=supervisor, callback_data=f"secondstatus_{i}")] for i, supervisor in enumerate(STATUS)]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard