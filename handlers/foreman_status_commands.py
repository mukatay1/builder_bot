import json
from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from config import STATUS
from database.main import SessionLocal
from database.models.Apartment import Apartment
from keyboards.status_keyboard import get_second_status_keyboard
from utils.calculate_percentage import calculate_completion_percentage
from utils.get_current_time import get_current_time
from utils.validate_apartment_number import validate_apartment_number


class NewForm(StatesGroup):
    apartment_number = State()


router = Router()


@router.message(lambda message: message.text == "Выбрать статус")
async def choose_stage(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер квартиры для выбора статуса.")
    await state.set_state(NewForm.apartment_number)


@router.message(NewForm.apartment_number)
async def stage_handle(message: types.Message, state: FSMContext):
    user_apartment_number = message.text
    await state.update_data(number=message.text)

    session = SessionLocal()

    error_message = validate_apartment_number(user_apartment_number)
    if error_message:
        await message.answer(error_message)
        await state.clear()

        return

    apartment = session.query(Apartment).filter_by(number=user_apartment_number).first()
    if not apartment:
        await message.answer("Квартира с таким номером не найдена.")
        await state.clear()
        return

    await message.answer("Пожалуйста, выберите статус.", reply_markup=get_second_status_keyboard())


@router.callback_query(lambda c: c.data.startswith('status_'))
async def handle_supervisor_status(callback_query: CallbackQuery, state: FSMContext):
    session = SessionLocal()
    data = await state.get_data()
    number = data.get("number")

    apartment = session.query(Apartment).filter_by(number=number).first()
    apartments = session.query(Apartment).all()

    try:
        status_index = int(callback_query.data.split('_', 1)[1])

        if status_index >= len(STATUS):
            await callback_query.message.answer("Пожалуйста, выберите статус.")
            return
        status = STATUS[status_index]
        apartment.status = status
        apartment.status_id = status_index + 1
        apartment.status_date = get_current_time()

        await callback_query.message.answer(
            f"*Квартира номер:* `{number}`\n"
            f"*Статус:* {status}\n",
            parse_mode="MarkdownV2"
        )
        session.commit()

        if not apartment.start_date:
            apartment.start_date = get_current_time()
            session.commit()


        completion_percentage = calculate_completion_percentage(apartments)
        current_percentage = completion_percentage.get(status, 0)

        if completion_percentage.get(status, 0) >= 100:
            completion_data = {
                "status_id": status_index,
                "completion_date": datetime.now().strftime("%Y-%m-%d")
            }
            try:
                with open('completion_data.json', 'r') as f:
                    existing_data = json.load(f)
            except Exception as e:
                print(e)
                existing_data = []

            existing_data.append(completion_data)

            with open('completion_data.json', 'w') as f:
                json.dump(existing_data, f, indent=4)

            await callback_query.message.answer(f"Статус {status} достиг 100% выполнения. Все завершено.")

        session.close()
        await state.clear()
    except Exception as e:
        print(f"Error in handle_supervisor: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке вашего выбора.")
