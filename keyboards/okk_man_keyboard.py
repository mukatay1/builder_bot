from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def okk_man_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Доступные квартиры: 1 этап")],
        [KeyboardButton(text="Доступные квартиры: 2 этап")],
        [KeyboardButton(text="Чистота производства")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
        one_time_keyboard=False

    )
    return keyboard
