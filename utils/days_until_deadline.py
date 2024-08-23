from datetime import datetime

from config import DEADLINE


def days_until_deadline():
    deadline_date = datetime.strptime(DEADLINE, "%Y-%m-%d")
    current_date = datetime.now()
    delta = (deadline_date - current_date).days

    if delta > 0:
        return f"До дедлайна осталось {delta} дней."
    elif delta < 0:
        return f"Дедлайн просрочен на {-delta} дней."
    else:
        return "Дедлайн сегодня!"

