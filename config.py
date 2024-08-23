import os

from dotenv import load_dotenv

from utils.string_to_list import string_to_list

load_dotenv()

DEBUG = True

FOREMAN = string_to_list(os.getenv('FOREMAN'))
OKK_MAN = string_to_list(os.getenv('OKK_MAN'))
REPORT_MAN = string_to_list(os.getenv('REPORT_MAN'))
ADMIN = string_to_list(os.getenv('ADMIN'))

DEADLINE = "2024-11-15"

STATUS = [
    'Черновая электрика и черновая сантехника',
    'Стены и наливной пол',
    'Укладка кафеля в с\у и на балкон',
    'Укладка ламината',
    'Обои и краска',
    'Установка дверей',
    'Натяжной потолок',
    'Установка чистовой сантехники и чистовой электрики'
]