from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import FOREMAN


def start_keyboard() -> ReplyKeyboardMarkup:

    kb = [
        [KeyboardButton(text="Нет доступа")],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку"
    )
    return keyboard

