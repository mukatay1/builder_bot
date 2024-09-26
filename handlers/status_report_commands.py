
from aiogram import Router, types
from aiogram.types import FSInputFile

from utils.create_status_report import generate_apartment_status_report

router = Router()


@router.message(lambda message: message.text == "Отчет статуса")
async def status_report_stage(message: types.Message):
    report_filename = generate_apartment_status_report(report_filename="Статус_отчет.xlsx")
    report_document = FSInputFile(report_filename)
    await message.answer_document(report_document, caption=f"Статус_отчет")