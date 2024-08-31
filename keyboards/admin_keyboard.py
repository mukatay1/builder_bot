from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="1 этап квартира"), KeyboardButton(text="Доступные квартиры: 1 этап")],
        [KeyboardButton(text="2 этап квартира"), KeyboardButton(text="Доступные квартиры: 2 этап")],
        [KeyboardButton(text="Выбрать статус"), KeyboardButton(text="Подробный отчет")],
        [KeyboardButton(text="Подписать АВР"), KeyboardButton(text="Чистота производства")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    return keyboard