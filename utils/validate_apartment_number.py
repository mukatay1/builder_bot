def validate_apartment_number(number: str) -> str:
    try:
        apartment_number = int(number)
        if not (100 <= apartment_number <= 242):
            return "Номер квартиры должен быть в пределах от 100 до 242."
    except ValueError:
        return "Введите корректный номер квартиры (целое число)."
    return None