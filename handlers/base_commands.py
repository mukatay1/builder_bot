from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from keyboards import *
from utils.get_user_role import get_user_role

router = Router()


@router.message(Command(commands=["start", "help"]))
async def start_handler(message: types.Message):
    role = get_user_role(message.from_user.id)

    if role == 'foreman':
        keyboard = foreman_keyboard()
    elif role == 'okk_man':
        keyboard = okk_man_keyboard()
    elif role == 'report_man':
        keyboard = report_man_keyboard()
    elif role == 'admin':
        keyboard = admin_keyboard()
    else:
        keyboard = start_keyboard()

    welcome_message = f"Добро пожаловать, {role.capitalize()}!"

    await message.answer(
        welcome_message,
        reply_markup=keyboard
    )

