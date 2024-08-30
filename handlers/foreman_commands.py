from aiogram import Router
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum
from utils.get_current_time import get_current_time
from utils.validate_apartment_number import validate_apartment_number

router = Router()


class Form(StatesGroup):
    apartment_number = State()


class SecondForm(StatesGroup):
    apartment_number = State()


@router.message(lambda message: message.text == "1 этап квартира")
async def start_first_stage(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер квартиры для 1 этапа.")
    await state.set_state(Form.apartment_number)


@router.message(Form.apartment_number)
async def handle_apartment_number(message: types.Message, state: FSMContext):
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

    first_stage = session.query(ApartmentStage).filter_by(apartment_id=apartment.id, stage=StageEnum.FIRST).first()
    if not first_stage:
        await message.answer("Первый этап для этой квартиры не найден.")
        await state.clear()
        return

    first_stage.is_ready_for_review = True
    first_stage.started = True
    session.commit()

    if not apartment.start_date:
        apartment.start_date = get_current_time()
        session.commit()

    await message.answer(
        f"*Квартира номер:* `{user_apartment_number}`\n"
        "*Статус:* 1 этап готов к принятию",
        parse_mode="MarkdownV2"
    )
    session.close()
    await state.clear()


@router.message(lambda message: message.text == "2 этап квартира")
async def start_second_stage(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер квартиры для 2 этапа.")
    await state.set_state(SecondForm.apartment_number)


@router.message(SecondForm.apartment_number)
async def handle_apartment_number_for_second_stage(message: types.Message, state: FSMContext):
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

    second_stage = session.query(ApartmentStage).filter_by(apartment_id=apartment.id, stage=StageEnum.SECOND).first()
    if not second_stage:
        await message.answer("Второй этап для этой квартиры не найден.")
        await state.clear()
        return

    second_stage.is_ready_for_review = True
    second_stage.started = True
    session.commit()

    if not apartment.start_date:
        apartment.start_date = get_current_time()
        session.commit()

    await message.answer(
        f"*Квартира номер:* `{user_apartment_number}`\n"
        "*Статус:* 2 этап готов к принятию",
        parse_mode="MarkdownV2"
    )
    session.close()
    await state.clear()



