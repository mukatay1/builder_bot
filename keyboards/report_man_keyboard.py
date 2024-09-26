from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def report_man_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Подробный отчет")],
        [KeyboardButton(text="Отчет статуса")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
        one_time_keyboard=False
    )
    return keyboard