import os

from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import SQLAlchemyError

from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum
from keyboards.okk_man_inline_keyboard import create_apartment_keyboard, create_second_apartment_keyboard

router = Router()


class Form(StatesGroup):
    media = State()


class SecondForm(StatesGroup):
    media = State()


@router.message(lambda message: message.text == "Доступные квартиры: 1 этап")
async def start_first_stage(message: types.Message):
    session = SessionLocal()
    keyboard = await create_apartment_keyboard(session)
    await message.answer("Доступные квартиры для первого этапа. Пожалуйста, выберите квартиру.", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('apartment_'))
async def handle_apartment_selection(callback_query: types.CallbackQuery, state: FSMContext):
    apartment_number = callback_query.data.split("_")[1]

    await state.update_data(selected_apartment=apartment_number)

    await callback_query.message.answer(
        f"Вы выбрали квартиру номер: {apartment_number}. Пожалуйста, отправьте фото или видео для первого этапа."
    )
    await state.set_state(Form.media)


@router.message(Form.media)
async def handle_media(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    apartment_number = user_data.get('selected_apartment')

    if not apartment_number:
        await message.answer("Ошибка: не выбран номер квартиры.")
        return

    if not os.path.exists(f"media/{apartment_number}"):
        os.makedirs(f"media/{apartment_number}")

    if message.photo:
        photo_id = message.photo[-1].file_id
        file = await bot.download(message.photo[-1], destination=f"media/{apartment_number}/photo_{photo_id}.jpg")
        await message.answer("Фото получено и сохранено.")
    elif message.video:
        video_id = message.video.file_id
        file = await bot.download(message.video, destination=f"media/{apartment_number}/video_{video_id}.mp4")
        await message.answer("Видео получено и сохранено.")
    else:
        await message.answer("Пожалуйста, отправьте фото или видео.")

    session = SessionLocal()
    try:
        apartment = session.query(Apartment).join(ApartmentStage).filter(Apartment.number == apartment_number,
                                                                         ApartmentStage.stage == StageEnum.FIRST).first()

        if apartment:
            stage = apartment.stages[0]
            stage.is_ready_for_review = False
            stage.is_finished = True
            session.commit()
        else:
            await message.answer("Ошибка: квартира не найдена.")
    except SQLAlchemyError as e:
        await message.answer(f"Ошибка базы данных: {e}")
    finally:
        session.close()

    await state.clear()


@router.message(lambda message: message.text == "Доступные квартиры: 2 этап")
async def start_first_stage(message: types.Message):
    session = SessionLocal()
    keyboard = await create_second_apartment_keyboard(session)
    await message.answer("Доступные квартиры для второго этапа. Пожалуйста, выберите квартиру.", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('secondapartment_'))
async def handle_apartment_selection(callback_query: types.CallbackQuery, state: FSMContext):
    apartment_number = callback_query.data.split("_")[1]
    await state.update_data(selected_apartment=apartment_number)

    await callback_query.message.answer(
        f"Вы выбрали квартиру номер: {apartment_number}. Пожалуйста, отправьте фото или видео для второго этапа."
    )
    await state.set_state(SecondForm.media)


@router.message(SecondForm.media)
async def handle_media(message: types.Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    apartment_number = user_data.get('selected_apartment')

    if not apartment_number:
        await message.answer("Ошибка: не выбран номер квартиры.")
        return

    if not os.path.exists(f"media/{apartment_number}"):
        os.makedirs(f"media/{apartment_number}")

    if message.photo:
        photo_id = message.photo[-1].file_id
        file = await bot.download(message.photo[-1], destination=f"media/{apartment_number}/photo_{photo_id}.jpg")
        await message.answer("Фото получено и сохранено.")
    elif message.video:
        video_id = message.video.file_id
        file = await bot.download(message.video, destination=f"media/{apartment_number}/video_{video_id}.mp4")
        await message.answer("Видео получено и сохранено.")
    else:
        await message.answer("Пожалуйста, отправьте фото или видео.")

    session = SessionLocal()
    try:
        apartment = session.query(Apartment).join(ApartmentStage).filter(Apartment.number == apartment_number,
                                                                         ApartmentStage.stage == StageEnum.SECOND).first()

        if apartment:
            stage = apartment.stages[1]
            stage.is_ready_for_review = False
            stage.is_finished = True
            session.commit()
        else:
            await message.answer("Ошибка: квартира не найдена.")
    except SQLAlchemyError as e:
        await message.answer(f"Ошибка базы данных: {e}")
    finally:
        session.close()

    await state.clear()