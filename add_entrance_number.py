from database.main import SessionLocal
from database.models.Apartment import Apartment
from database.models.ApartmentStage import ApartmentStage


def reset_apartment_stages():
    session = SessionLocal()
    try:
        # Определение диапазонов квартир
        apartments_entrance_3 = list(range(100, 172))  # 3 подъезд: квартиры от 100 до 171
        apartments_entrance_4 = list(range(172, 243))  # 4 подъезд: квартиры от 172 до 242

        # Получение квартир для 3 подъезда
        apartments_3 = session.query(Apartment).filter(Apartment.number.in_(apartments_entrance_3)).all()
        for apartment in apartments_3:
            stages = session.query(ApartmentStage).filter_by(apartment_id=apartment.id).all()

            apartment.entrance_number = 3

        apartments_4 = session.query(Apartment).filter(Apartment.number.in_(apartments_entrance_4)).all()

        for apartment in apartments_4:
            stages = session.query(ApartmentStage).filter_by(apartment_id=apartment.id).all()

            apartment.entrance_number = 4

        # Коммит изменений в базе данных
        session.commit()
        print('Квартиры успешно обновлены.')

    except Exception as e:
        session.rollback()  # Откат изменений в случае ошибки
        print(f'Произошла ошибка: {e}')

    finally:
        session.close()  # Закрытие сессии


# Вызов функции
reset_apartment_stages()
