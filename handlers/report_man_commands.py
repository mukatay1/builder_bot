from aiogram import Router, types
from aiogram.types import FSInputFile

from utils.create_report import generate_apartment_stage_report
from utils.create_simple_report import generate_apartment_stage_simple_report

router = Router()


@router.message(lambda message: message.text == "Отчет")
async def start_first_stage(message: types.Message):
    report_filename = generate_apartment_stage_simple_report(report_filename="Отчет.xlsx")
    report_document = FSInputFile(report_filename)
    await message.answer_document(report_document, caption=f"Отчет")


@router.message(lambda message: message.text == "Подробный отчет")
async def start_first_stage(message: types.Message):
    report_filename = generate_apartment_stage_report(report_filename="Подробный отчет.xlsx")
    report_document = FSInputFile(report_filename)
    await message.answer_document(report_document, caption=f"Подробный отчет")