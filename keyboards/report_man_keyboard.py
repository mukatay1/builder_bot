from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def report_man_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Подробный отчет")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    return keyboard