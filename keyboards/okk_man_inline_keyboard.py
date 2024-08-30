from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum


async def create_apartment_keyboard(session: Session) -> InlineKeyboardMarkup:
    try:
        apartments = session.query(Apartment).join(Apartment.stages).filter(
            ApartmentStage.stage == StageEnum.FIRST,
            ApartmentStage.is_ready_for_review == True
        ).all()

        kb = []

        for apartment in apartments:
            apartment_number = apartment.number
            button = InlineKeyboardButton(
                text=f"Квартира {apartment_number}",
                callback_data=f"apartment_{apartment_number}"
            )
            kb.append([button])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        return keyboard

    except SQLAlchemyError as e:
        print(f"Error fetching apartments: {e}")
        return InlineKeyboardMarkup()


async def create_second_apartment_keyboard(session: Session) -> InlineKeyboardMarkup:
    try:
        apartments = session.query(Apartment).join(Apartment.stages).filter(
            ApartmentStage.stage == StageEnum.SECOND,
            ApartmentStage.is_ready_for_review == True
        ).all()

        kb = []

        for apartment in apartments:
            apartment_number = apartment.number
            button = InlineKeyboardButton(
                text=f"Квартира {apartment_number}",
                callback_data=f"secondapartment_{apartment_number}"
            )
            kb.append([button])

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        return keyboard

    except SQLAlchemyError as e:
        print(f"Error fetching apartments: {e}")
        return InlineKeyboardMarkup()


def accept_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Принять", callback_data="Принять"),
         InlineKeyboardButton(text="Не принять", callback_data="Отклонить")],

    ]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard