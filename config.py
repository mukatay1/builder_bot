import os

from dotenv import load_dotenv
from openpyxl.styles import PatternFill, Border, Side

from utils.string_to_list import string_to_list

load_dotenv()

DEBUG = False

FOREMAN = string_to_list(os.getenv('FOREMAN'))
OKK_MAN = string_to_list(os.getenv('OKK_MAN'))
REPORT_MAN = string_to_list(os.getenv('REPORT_MAN'))
ADMIN = string_to_list(os.getenv('ADMIN'))

DEADLINE = "2024-11-15"

STATUS = [
    'Черновая электрика и черновая сантехника',
    'Стены',
    'Подоконник/откосы',
    'Укладка с\у и балкона',
    'Наливной пол',
    'Укладка ламината',
    'Обои',
    'Установка дверей',
    'Натяжной потолок',
    'Установка чистовой электрики и чистовой сантехники',
    'Покраска стен',
    'Клининг'
]

MAX_STATUS_NUMBER = 12

red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
green_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

black_border = Border(
    left=Side(border_style='thin', color='000000'),
    right=Side(border_style='thin', color='000000'),
    top=Side(border_style='thin', color='000000'),
    bottom=Side(border_style='thin', color='000000')
)

NUMBERS = [1, 2, 3, 4, 5]
lst = FOREMAN + OKK_MAN + REPORT_MAN + ADMIN
USERS = [user_id for user_id in lst if user_id]
