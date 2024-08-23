import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.cell import MergedCell

from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import StageEnum


def generate_apartment_stage_report(report_filename: str):
    session = SessionLocal()
    apartments = session.query(Apartment).all()

    data = []
    for apartment in apartments:
        first_stage = next((stage for stage in apartment.stages if stage.stage == StageEnum.FIRST), None)
        second_stage = next((stage for stage in apartment.stages if stage.stage == StageEnum.SECOND), None)

        data.append({
            "Номер квартиры": apartment.number,
            "Первый этап готов": 'Принят' if (first_stage and first_stage.is_finished) else 'Нет',
            "Второй этап готов": 'Принят' if (second_stage and second_stage.is_finished) else 'Нет',
            "Статус": apartment.status
        })

    df = pd.DataFrame(data)

    df.to_excel(report_filename, index=False, engine='openpyxl')

    wb = load_workbook(report_filename)
    ws = wb.active
    ws.title = "Отчет по этапам"

    ws.insert_rows(1)
    ws.merge_cells('A1:D1')
    ws['A1'] = 'Отчет по готовности этапов квартир'
    ws['A1'].font = Font(size=16, bold=True)

    for column in ws.columns:
        max_length = 0
        column_letter = None
        for cell in column:
            if not isinstance(cell, MergedCell):
                column_letter = cell.column_letter
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
        if column_letter:
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width

    wb.save(report_filename)

    return report_filename
