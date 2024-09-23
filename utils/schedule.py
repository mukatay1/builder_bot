import schedule
import asyncio
from aiogram import Bot

from config import USERS
from utils.calculate_percent import calculate_percentage_for_apartments
from utils.days_until_deadline import days_until_deadline


def format_percentage_with_bar(percent):
    total_blocks = 10
    filled_blocks = int(percent // 10)
    empty_blocks = total_blocks - filled_blocks
    progress_bar = "█" * filled_blocks + "░" * empty_blocks
    return f"<b>Завершено: {percent:.2f}%</b> [{progress_bar}]"


async def send_morning_message(bot: Bot) -> None:
    try:
        deadline = days_until_deadline()
        percent = calculate_percentage_for_apartments(100, 242)
        message_text = (
            f"<b>🕰️ Доброе утро!</b>\n\n"
            f"<b>Крайний срок:</b> {deadline}\n"
            f"{format_percentage_with_bar(percent)}"
        )
        print(USERS)
        for telegram_id in USERS:
            try:
                await bot.send_message(telegram_id, message_text)
            except Exception as e:
                print(f"Не удалось отправить сообщение сотруднику {telegram_id}: {e}")
    except Exception as e:
        print(f"Ошибка при отправке сообщений: {e}")



async def run_schedule() -> None:
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


def schedule_jobs(bot: Bot) -> None:
    schedule.every().monday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().tuesday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().wednesday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().thursday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().friday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().saturday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))
    schedule.every().sunday.at("09:00").do(lambda: asyncio.create_task(send_morning_message(bot)))

    loop = asyncio.get_event_loop()
    loop.create_task(run_schedule())