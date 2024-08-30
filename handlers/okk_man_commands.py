import os

from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.exc import SQLAlchemyError

from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum
from keyboards.okk_man_inline_keyboard import create_apartment_keyboard, create_second_apartment_keyboard, \
    accept_keyboard
from utils.get_current_time import get_current_time
from utils.validate_apartment_number import validate_apartment_number

router = Router()


class Form(StatesGroup):
    media = State()
    comment = State()


class SecondForm(StatesGroup):
    media = State()


class WorkForm(StatesGroup):
    work_apartment_number = State()

@router.message(lambda message: message.text == "Доступные квартиры: 1 этап")
async def start_first_stage(message: types.Message):
    session = SessionLocal()
    keyboard = await create_apartment_keyboard(session)
    await message.answer("Доступные квартиры для первого этапа. Пожалуйста, выберите квартиру.", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('apartment_'))
async def handle_apartment_selection(callback_query: types.CallbackQuery, state: FSMContext):
    apartment_number = callback_query.data.split("_")[1]

    await state.update_data(selected_apartment=apartment_number, stage=StageEnum.FIRST)
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
           # stage.is_ready_for_review = False
            session.commit()
        else:
            await message.answer("Ошибка: квартира не найдена.")
    except SQLAlchemyError as e:
        await message.answer(f"Ошибка базы данных: {e}")
    finally:
        session.close()

    keyboard = accept_keyboard()
    await message.answer(f'Принять 1 этап для квартиры №{apartment_number}?', reply_markup=keyboard)


@router.callback_query(lambda message: message.data == "Принять")
async def handle_accept(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    apartment_number = user_data.get('selected_apartment')
    stage_enum_value = user_data.get('stage')

    session = SessionLocal()

    try:
        apartment = session.query(Apartment).filter_by(number=apartment_number).first()

        if apartment:
            stage = session.query(ApartmentStage).filter_by(apartment_id=apartment.id, stage=stage_enum_value).first()
            apartment.end_date = get_current_time()
            session.commit()

            if stage:
                stage.is_finished = True
                stage.is_ready_for_review = False
                session.commit()
                await callback_query.message.answer("Этап успешно завершён!")
            else:
                await callback_query.message.answer("Ошибка: этап не найден.")
        else:
            await callback_query.message.answer("Ошибка: квартира не найдена.")

    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()
        session.close()


@router.callback_query(lambda message: message.data == "Отклонить")
async def handle_accept(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Укажите причину отказа от принятия.")
    await state.set_state(Form.comment)


@router.message(Form.comment)
async def handle_comment(message: types.Message, state: FSMContext):
    comment = message.text
    user_data = await state.get_data()
    apartment_number = user_data.get('selected_apartment')
    stage_enum_value = user_data.get('stage')

    session = SessionLocal()
    try:
        apartment = session.query(Apartment).filter_by(number=apartment_number).first()

        if apartment:
            stage = session.query(ApartmentStage).filter_by(apartment_id=apartment.id, stage=stage_enum_value).first()

            if stage:
                stage.is_ready_for_review = False
                stage.comment = comment

                session.commit()
                await message.answer("Причина отклонения этапа успешно записана.")
            else:
                await message.answer("Ошибка: этап не найден.")
        else:
            await message.answer("Ошибка: квартира не найдена.")

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()
        session.close()


@router.message(lambda message: message.text == "Доступные квартиры: 2 этап")
async def start_first_stage(message: types.Message):
    session = SessionLocal()
    keyboard = await create_second_apartment_keyboard(session)
    await message.answer("Доступные квартиры для второго этапа. Пожалуйста, выберите квартиру.", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('secondapartment_'))
async def handle_apartment_selection(callback_query: types.CallbackQuery, state: FSMContext):
    apartment_number = callback_query.data.split("_")[1]
    await state.update_data(selected_apartment=apartment_number, stage=StageEnum.SECOND)

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
            #stage.is_ready_for_review = False
            session.commit()
        else:
            await message.answer("Ошибка: квартира не найдена.")
    except SQLAlchemyError as e:
        await message.answer(f"Ошибка базы данных: {e}")
    finally:
        session.close()

    keyboard = accept_keyboard()

    await message.answer(f'Принять 2 этап для квартиры №{apartment_number}?', reply_markup=keyboard)


@router.message(lambda message: message.text == "Подписать АВР")
async def handle_work_accepted(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите номер квартиры для подписания АВР.")
    await state.set_state(WorkForm.work_apartment_number)


@router.message(WorkForm.work_apartment_number)
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

    apartment.is_accepted = True
    session.commit()

    await message.answer(
        f"*Квартира номер:* `{user_apartment_number}`\n"
        f"*Статус:* АВР подписан для квартиры №{user_apartment_number}\\.",
        parse_mode="MarkdownV2"
    )
    session.close()
    await state.clear()
