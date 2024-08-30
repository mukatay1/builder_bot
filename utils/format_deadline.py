from datetime import datetime

from config import DEADLINE


def format_deadline_date():
    deadline_date = datetime.strptime(DEADLINE, "%Y-%m-%d")
    return deadline_date.strftime("%d.%m.%y")