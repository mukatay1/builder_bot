from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def foreman_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="1 этап квартира"), KeyboardButton(text="2 этап квартира")],
        [KeyboardButton(text="Выбрать статус"), KeyboardButton(text="Подписать АВР")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
        one_time_keyboard=False

    )
    return keyboard