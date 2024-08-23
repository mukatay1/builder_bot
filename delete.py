from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum


def reset_apartment_stages():
    session = SessionLocal()

    apartment_numbers = ['100', '101', '109', '110', '177', '199']

    apartments = session.query(Apartment).filter(Apartment.number.in_(apartment_numbers)).all()

    for apartment in apartments:
        stages = session.query(ApartmentStage).filter_by(apartment_id=apartment.id).all()
        for stage in stages:
            stage.is_ready_for_review = False
            stage.is_finished = False
            stage.started = False
        apartment.status = ''
    session.commit()

if __name__ == "__main__":
    reset_apartment_stages()
    print("Apartment stages have been reset.")