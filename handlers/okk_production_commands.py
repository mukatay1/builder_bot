from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import NUMBERS
from database.main import SessionLocal
from database.models.Apartment import Apartment
from keyboards.get_number_keyboard import get_number_keyboard
from utils.validate_apartment_number import validate_apartment_number

router = Router()


class ProductionForm(StatesGroup):
    production_apartment_number = State()


@router.message(lambda message: message.text == "Чистота производства")
async def handle_work_accepted(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер квартиры для чистоты производства.")
    await state.set_state(ProductionForm.production_apartment_number)


@router.message(ProductionForm.production_apartment_number)
async def handle_apartment_number(message: types.Message, state: FSMContext):
    user_apartment_number = message.text
    await state.update_data(apartment_number=message.text)
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

    session.close()
    await message.answer("Пожалуйста, выберите уровень чистоты производства.", reply_markup=get_number_keyboard())


@router.callback_query(lambda c: c.data.startswith('number_'))
async def handle_supervisor_status(callback_query: types.CallbackQuery, state: FSMContext):
    session = SessionLocal()
    data = await state.get_data()
    apartment_number = data.get('apartment_number')

    apartment = session.query(Apartment).filter_by(number=apartment_number).first()

    try:
        number_index = int(callback_query.data.split('_', 1)[1])
        print(number_index)
        if number_index >= len(NUMBERS):
            await callback_query.message.answer("Пожалуйста, выберите номер.")
            return

        number = NUMBERS[number_index]

        if apartment:
            apartment.clear_level = number
            session.commit()
        else:
            await state.clear()
            await callback_query.message.answer("Квартира с таким номером не найдена.")

        await callback_query.message.answer(
            f"*Квартира номер:* `{apartment_number}`\n"
            f"*Чистота производства:* {number}\n",
            parse_mode="MarkdownV2"
        )
        session.close()
        await state.clear()

    except Exception as e:
        print(f"Error in handle_supervisor: {e}")
        await callback_query.message.answer("Произошла ошибка при обработке вашего выбора.")
