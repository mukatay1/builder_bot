from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage, StageEnum


def reset_apartment_stages():
    session = SessionLocal()

    apartment_numbers = ['110']

    apartments = session.query(Apartment).filter(Apartment.number.in_(apartment_numbers)).all()

    for apartment in apartments:
        apartment.end_date = None
    session.commit()

if __name__ == "__main__":
    reset_apartment_stages()
    print("Apartment stages have been reset.")