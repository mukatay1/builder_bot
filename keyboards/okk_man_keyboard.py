from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def okk_man_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Доступные квартиры: 1 этап")],
        [KeyboardButton(text="Доступные квартиры: 2 этап")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    return keyboard
