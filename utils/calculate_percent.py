from config import MAX_STATUS_NUMBER
from database.main import SessionLocal
from database.models.Apartment import Apartment


def calculate_percentage_for_apartments(start_number: int, end_number: int):
    with SessionLocal() as session:
        apartments = session.query(Apartment).filter(
            Apartment.number.between(start_number, end_number)
        ).all()

        total_apartments = len(apartments)
        if total_apartments == 0:
            return 0

        status_count = {}
        for apartment in apartments:
            status_id = apartment.status_id if apartment.status_id is not None else 0
            if status_id in status_count:
                status_count[status_id] += 1
            else:
                status_count[status_id] = 1

        sum_statuses = sum(status * count for status, count in status_count.items())

        apartments_with_zero_status = total_apartments - sum(status_count.values())

        max_possible_sum = total_apartments * int(MAX_STATUS_NUMBER)

        total_sum_statuses = sum_statuses + (apartments_with_zero_status * 0)

        completion_percentage = (total_sum_statuses / max_possible_sum) * 100

        return round(completion_percentage, 2)




