from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum

for i in range(100, 243):
    session = SessionLocal()
    apartment_number = i
    new_apartment = Apartment(number=apartment_number)
    session.add(new_apartment)
    session.commit()

    stage_first = ApartmentStage(
        stage=StageEnum.FIRST,
        is_ready_for_review=False,
        apartment_id=new_apartment.id
    )

    stage_second = ApartmentStage(
        stage=StageEnum.SECOND,
        is_ready_for_review=False,
        apartment_id=new_apartment.id
    )

    session.add(stage_first)
    session.add(stage_second)

    session.commit()

print("142 apartments with stages for both stages and review flags have been added.")