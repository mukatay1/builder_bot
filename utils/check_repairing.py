from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import StageEnum


def count_apartments_with_conditions() -> int:
    session = SessionLocal()
    count = 0
    apartments = session.query(Apartment).all()

    for apartment in apartments:
        first_stage = next((stage for stage in apartment.stages if stage.stage == StageEnum.FIRST), None)
        second_stage = next((stage for stage in apartment.stages if stage.stage == StageEnum.SECOND), None)

        if (first_stage.started or second_stage.started) and (second_stage and not second_stage.is_finished):
            count += 1

    return count
